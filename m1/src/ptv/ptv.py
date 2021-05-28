import time

import numpy as np
import pandas as pd


class PTV(object):

    def __init__(self):
        pass

    def tracking(self):
        pass

    def four(self):
        pass

    def three(self):
        pass


def calc_gap(dx1, dx2):
    gap = np.hypot(dx2['x'] - dx1['x'], dx2['y'] - dx1['y'])

    inner_product = dx1['x'] * dx2['x'] + dx1['y'] * dx2['y']
    inner_product /= np.hypot(dx1['x'], dx1['y']) * np.hypot(dx2['x'], dx2['y'])
    if inner_product > 1.0:
        inner_product /= np.abs(inner_product)

    angle = np.arccos(inner_product)

    outer_product = dx1['x'] * dx2['y'] - dx1['y'] * dx2['x']
    if outer_product < 0:
        angle *= -1.0

    return gap, angle


def rot(_dx, angle):
    x = _dx['x'] * np.cos(angle) - _dx['y'] * np.sin(angle)
    y = _dx['x'] * np.sin(angle) + _dx['y'] * np.cos(angle)

    return x, y


if __name__ == '__main__':
    d = '../../../data/out/csv'
    pp0 = pd.read_csv(d + '/pp/' + '_00000000.csv').values[:, 1:]
    pp1 = pd.read_csv(d + '/pp/' + '_00000000.csv').values[:, 1:]
    pp2 = pd.read_csv(d + '/pp/' + '_00000000.csv').values[:, 1:]
    pp3 = pd.read_csv(d + '/pp/' + '_00000000.csv').values[:, 1:]

    nump = [len(pp0), len(pp1), len(pp2), len(pp3)]  # The number of particle in each file
    pp12 = [{'p1': 0, 'p2': 0, 'err': 0.0, 'flag': 0}] * nump[0]  # The number of available particle
    dx = [{'x': 0, 'y': 0}] * 3
    s1, s2 = 20.0, 14.0  # 1st and 2nd search range
    et = 13.0  # criterion on angle [deg]
    cf, cfc = 0, 0  # criterion factor
    npa = -1  # The number of available particle
    ntsp = 0  # the number for tracking the same particle

    # gap: gap between particle position and estimated particle position
    # angle: angle between particle position and estimated particle position
    dst = [{'gap': 0, 'angle': 0}] * 2

    start = time.time()
    for ii in range(0, nump[0]):  # 1st img
        print(f"{ii + 1} / {nump[0]}\ttime: {time.time() - start}\n")
        start = time.time()

        flag = 0  # clearing the flag for the particle tracking
        cf = 5000.0  # arbitrary large number
        for jj in range(0, nump[1]):  # 2nd img
            dx[0]['x'] = pp1[jj][0] - pp0[ii][0]
            dx[0]['y'] = pp1[jj][1] - pp0[ii][1]
            distance = np.hypot(dx[0]['x'], dx[0]['y'])

            if distance <= s1:
                for kk in range(0, nump[2]):  # 3rd img
                    dx[1]['x'] = pp2[kk][0] - pp1[jj][0]
                    dx[1]['y'] = pp2[kk][1] - pp1[jj][1]
                    dst[0]['gap'], dst[0]['angle'] = calc_gap(dx[0], dx[1])
                    dx[1]['x'], dx[1]['y'] = rot(dx[1], dst[0]['angle'])  # rotation of difference vector

                    if dst[0]['gap'] <= s2 and np.abs(dst[0]['angle']*180/np.pi) <= et:
                        for ll in range(0, nump[3]):  # 4th img
                            dx[2]['x'] = pp3[ll][0] - pp2[kk][0]
                            dx[2]['y'] = pp3[ll][1] - pp2[kk][1]
                            dst[1]['gap'], dst[1]['angle'] = calc_gap(dx[1], dx[2])
                            cfc = dst[0]['gap']**2 + dst[1]['gap']**2

                            if dst[1]['gap'] <= s2 and np.abs(dst[1]['angle']*180/np.pi) <= et and cfc < cf:
                                cf = cfc

                                if flag == 0:
                                    npa += 1

                                pp12[npa]['p1'] = ii
                                pp12[npa]['p2'] = jj  # position of the tracked particle
                                pp12[npa]['err'] = cf
                                pp12[npa]['flag'] = 0
                                flag += 1

    npa += 1
    print(f"\nThe number of available particle: {npa}\n")

    # post processing
    for ii in range(0, npa):
        if pp12[ii]['flag'] == 0:
            for jj in range(ii+1, npa):
                if pp12[ii]['p2'] == pp12[jj]['p2']:
                    # If different particles track the same particle,
                    # giving an error flag to particle which has larger error
                    if pp12[ii]['err'] > pp12[jj]['err']:
                        pp12[ii]['flag'] = 1
                        ntsp += 1
                        break

                    else:
                        pp12[jj]['flag'] = 1
                        ntsp += 1

    print(f"The number for tracking the same particle: {ntsp}\n")
    print(f"The number of remaining particle by post processing: {npa - ntsp}\n")

    # displacement
    save_data = np.array([[0, 1, 2, 3]])

    for ii in range(0, npa):
        if pp12[ii]['flag'] == 0:
            xp = pp0[pp12[ii]['p1']][0]
            yp = pp0[pp12[ii]['p1']][1]
            dxp = pp1[pp12[ii]['p2']][0] - pp0[pp12[ii]['p1']][0]
            dyp = pp1[pp12[ii]['p2']][1] - pp0[pp12[ii]['p1']][1]

            tmp_data = np.array([[xp, yp, dxp, dyp]])
            save_data = np.apend(save_data, tmp_data, axis=1)

    cols = ['x', 'y', 'dx', 'dy']
    save_df = pd.DataFrame(save_data, columns=cols)
    save_df.to_csv(d + '/dx/' + '0.csv', index=False)

    print(0)
