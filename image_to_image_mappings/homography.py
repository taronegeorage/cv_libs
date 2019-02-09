import numpy as np

def normalize(points):
    """ Normalize a collection of points in
    homogeneous coordinates so that last row = 1. """
    for row in points:
        row /= points[-1]
    return points
    
def make_homog(points):
    """ Convert a set of points (dim*n array) to
    homogeneous coordinates. """
    return vstack((points,ones((1,points.shape[1]))))


def H_from_points(fp,tp):
    """ Find homography H, such that fp is mapped to tp
    using the linear DLT method. Points are conditioned
    automatically. """
    if fp.shape != tp.shape:
        raise RuntimeError(’number of points do not match’)

    # condition points (important for numerical reasons)
    # --from points--
    m = mean(fp[:2], axis=1)
    maxstd = max(std(fp[:2], axis=1)) + 1e-9
    C1 = diag([1/maxstd, 1/maxstd, 1])
    C1[0][2] = -m[0]/maxstd
    C1[1][2] = -m[1]/maxstd
    fp = dot(C1,fp)
    # --to points--
    m = mean(tp[:2], axis=1)
    maxstd = max(std(tp[:2], axis=1)) + 1e-9
