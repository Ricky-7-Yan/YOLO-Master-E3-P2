import pytest
import torch
from torch import nn

from e3_p2.capture import SpatialRouterCollector, max_output_delta


class _MoTRouter(nn.Module):
    def forward(self, x, return_logits=True):
        del return_logits
        logits = torch.stack((x[:, 0], -x[:, 0], x[:, 0] * 0), dim=1)
        dense = torch.softmax(logits, dim=1)
        top_weights, indices = torch.topk(dense, 2, dim=1)
        top_weights = top_weights / top_weights.sum(dim=1, keepdim=True)
        weights = torch.zeros_like(dense).scatter(1, indices, top_weights)
        return weights, indices, logits


class TinyMoT(nn.Module):
    def __init__(self):
        super().__init__()
        self.router = _MoTRouter()

    def forward(self, x):
        weights, _, _ = self.router(x, return_logits=True)
        return x * weights[:, :1]


def test_hook_captures_real_spatial_grid_without_changing_output():
    model = TinyMoT().eval()
    value = torch.randn(1, 2, 4, 5)
    reference = model(value)
    collector = SpatialRouterCollector(family="mot", router_class="_MoTRouter")
    assert collector.register(model) == ["router"]
    observed = model(value)
    collector.remove()
    assert max_output_delta(reference, observed) == 0.0
    assert not collector.handles
    assert len(collector.records) == 1
    assert collector.records[0].weights.shape == (1, 3, 4, 5)
    assert collector.records[0].indices.shape == (1, 2, 4, 5)
    assert collector.records[0].validation["indices_in_range"] is True
    assert collector.records[0].validation["selected_mass_error"] < 1e-5


def test_output_equivalence_detects_structure_shape_and_value_changes():
    value = torch.zeros(1, 2)
    assert max_output_delta((value,), (value.clone(),)) == 0.0
    assert max_output_delta((value,), (value + 1,)) == 1.0
    with pytest.raises(ValueError, match="tensor count"):
        max_output_delta((value,), (value, value))
    with pytest.raises(ValueError, match="shape changed"):
        max_output_delta((value,), (torch.zeros(2, 1),))


def test_collector_rejects_non_spatial_router_output():
    class _MoARouter(nn.Module):
        def forward(self, x):
            weights = torch.softmax(x.mean((2, 3)), dim=1)
            return weights, weights

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.router = _MoARouter()

        def forward(self, x):
            return self.router(x)

    model = Model()
    collector = SpatialRouterCollector(family="moa", router_class="_MoARouter")
    collector.register(model)
    with pytest.raises(ValueError, match="expected"):
        model(torch.randn(1, 3, 4, 4))
    collector.remove()
