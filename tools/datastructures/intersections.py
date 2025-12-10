from tools.datastructures.points import Rectangle, Segment, Point2


def intersect_segment_segment(l1: Segment, l2: Segment) -> bool:
    l1_vert = l1.p1.x == l1.p2.x
    l2_vert = l2.p1.x == l2.p2.x
    match l1_vert, l2_vert:
        case False, True:
            intersection = Point2(l2.p1.x, l1.p1.y)
            return l1.contains(intersection) and l2.contains(intersection)
        case True, False:
            intersection = Point2(l1.p1.x, l2.p1.y)
            return l1.contains(intersection) and l2.contains(intersection)
        case _:
            return l1.contains(l2.p1) or l1.contains(l2.p2)


def intersect_rect_segment(r: Rectangle, s: Segment) -> bool:
    return (r.contains(s.p1) and r.contains(s.p2)) or any(intersect_segment_segment(rs, s) for rs in r.get_segments())
