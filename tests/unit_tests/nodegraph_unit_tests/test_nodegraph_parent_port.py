import pytest


@pytest.mark.skip
def test_parent_port(session, cmds, registry, model):
    """Validate 2 nodes in a hyerarchy have a `parent` and `children` ports."""
    n1 = session.create_node('transform', name='parent')
    n2 = session.create_node('transform', name='child')
    n1.set_parent(n2)

    registry.scan_session()
    model.add_all()

    port_names = [port.name for port in model.get_ports()]
    assert 'parent' in port_names
    assert 'children' in port_names
