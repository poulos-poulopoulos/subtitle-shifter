def trans_srt(state=0, inp=''):

    if state is not 1 and inp is '':
        state = 1
    elif state is 1 and inp.isdecimal():
        state = 2
    elif state is 2 and not inp.isdecimal():
        state = 'ready'
    elif state is 'ready':
        state = 0
    return state


def trans_vtt(state=10, inp=None):

    if state is 10 and inp is '':
        state = 11
    elif state is 11:
        if (inp.startswith('NOTE') or
            inp.startswith('STYLE') or
            inp.startswith('REGION')):
            state = 10
        elif ' --> ' in inp:
            state = 'ready'
    elif state in (0, 'ready') and inp is '':
        state = 1
    elif state is 1:
        if inp.startswith('NOTE'):
            state = 0
        elif ' --> ' in inp:
            state = 'ready'
    elif state is 'ready':
        state = 0
    return state


def shift_subs():

    def read(line):

        return (lambda moments, *rest: ([list(map(int,
                                                  (lambda x, y: [*x.split(':'), y])(
                                                      *moment.split(sep))))
                                         for moment in moments],
                                        *rest))(
                   *(lambda x, y: ([x, y[0]], *y[1:]))(
                       *(lambda x, y: (x, y.partition(' ')))(
                           *line[:-1].split(' --> '))))

    def write(moments, space, settings):

        return space.join((' --> '.join(sep.join((':'.join(str(m).zfill(2)
                                                           for m in moment[:-1]),
                                                  str(moment[-1]).zfill(3)))
                                        for moment in moments),
                           settings)) + '\n'

    def lshift(moment):

        moment_ = []
        car = False
        for m, t, l in zip(moment[::-1], time[::-1], lim[::-1]):
            m -= t
            if car:
                m -= 1
            if m < 0:
                m += l
                car = True
            else:
                car = False
            moment_[0:0] = [m]
        return moment_

    def rshift(moment):

        moment_ = []
        car = False
        for m, t, l in zip(moment[::-1], time[::-1], lim[::-1]):
            m += t
            if car:
                m += 1
            if m >= l:
                m -= l
                car = True
            else:
                car = False
            moment_[0:0] = [m]
        return moment_


    lim = (24, 60, 60, 1000)
    from sys import argv
    rw = '-rw' in argv

    while True:

        fname = input('file name: ')
        if not fname: break
        fname, _, fext = fname.rpartition('.')
        trans = {'srt': trans_srt, 'vtt': trans_vtt}[fext]
        sep = {'srt': ',', 'vtt': '.'}[fext]

        fname_ = input('new name: ')
        if not fname_:
            fname_ = fname + '-'
        elif fname_[0] is '*':
            fname_ = fname + fname_[1:]
        fsame = fname_ == fname

        time = input('time interval: ')
        shift = (lambda shift: lambda moments, *rest: (map(shift, moments), *rest))(
                    {'-': lshift, '+': rshift}[time[0]])
        time = [0 if not t else int(t) for t in time[1:].split(',')]
        time[0:0] = [0] * (4 - len(time))

        print()

        state = trans()
        if rw and fsame:
            with open(fname_ + '.' + fext, 'r+',
                      encoding='utf-8-sig', errors='surrogateescape') as f:
                while True:
                    pos = f.tell()
                    line = f.readline()
                    if not line: break
                    state = trans(state, line[:-1])
                    if state is 'ready':
                        f.seek(pos)
                        f.write(write(*shift(*read(line))))
        else:
            f = open(fname + '.' + fext, 'r',
                     encoding='utf-8-sig', errors='surrogateescape')
            inp = f.readlines() if fsame else f
            if fsame:
                f.close()
            with open(fname_ + '.' + fext, 'w',
                      encoding='utf-8', errors='surrogateescape') as f:
                for line in inp:
                    state = trans(state, line[:-1])
                    f.write(line
                            if state is not 'ready' else
                            write(*shift(*read(line))))
            if not fsame:
                inp.close()


if __name__ == '__main__':
    shift_subs()
