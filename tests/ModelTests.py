import Model


def test_truck():
    truck = Model.Truck()
    print('Testing truck class.')
    print(truck)
    assert (truck.AVG_MPH == 18)
    assert (truck.DELIVERY_TIME_SECONDS == 0.0)
    assert (truck.MAX_LOAD == 16)


# def test_package():
#     package = Model.Package(package_id=0, package_weight=0.0, special_note='Test note',
#                             delivery_address='Test Address',
#                             delivery_city='Test City', delivery_zip='00000', delivery_deadline=0)
#     print('Testing Package class.')
#     print(package)
#     assert (package.package_weight == 0.0)
#     assert (package.delivery_address == 'Test Address')
#     assert (package.delivery_city == 'Test City')
#     assert (package.delivery_deadline == 0)
#     assert (package.delivery_zip == '00000')
#     assert (package.package_id == 0)
#     assert (package.special_note == 'Test note')


# TODO: Test loading of packages
# for i in package_list:
#     print(i)
# TODO: Move distances loading to unit test
# for i in distance_graph.edge_weights.items():
#      print(i[0][0], ', ', i[0][1], ', ', i[1])

# TODO: Move path testing to unit tests
# for v in distance_graph.adjacency_list:
#     if v.predecessor is None and v is not distance_graph.hub_vertex:
#         print("HUB to %s: no path exists" % v.label)
#     else:
#         print(" to %s: %s (total weight: %g)" % (
#               v.label, ShortestPath.get_shortest_path(distance_graph.hub_vertex, v), v.distance))


# TODO: Move to unit tests
# print('======={0}: ================='.format(v.label))
# for adj_v in distance_graph.adjacency_list[v]:
#     print(adj_v.label, ' : ', adj_v.distance)

# for key in distance_graph.adjacency_list:
#     for v in distance_graph.adjacency_list[key]:
#         print(ShortestPath.get_shortest_path(key, v))
