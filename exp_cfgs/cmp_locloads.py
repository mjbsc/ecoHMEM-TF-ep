import argparse
import re

def parse_location_translations(fname):
    data = [[]]
    with open(fname) as fin:
        for l in fin:
            l = l.rstrip()
            if l == '':
                continue
            
            #if 'Updating code locations' in l:
            if 'Raw locations information:' in l:
                data.append(list())
            elif l.startswith('FLEXMALLOC|* Location') and l.endswith(']'):
                #data[-1].append(l)
                m = re.match(r"FLEXMALLOC\|\* Location (?P<idx>\d+) on allocator '(?P<allocator>[^']+)' with \d+ frames: \[ (?P<frames>[0-9a-fA-F >]+?) \]$", l)
                if m is not None:
                    data[-1].append({
                        'idx': int(m.group('idx')),
                        'allocator': m.group('allocator'),
                        'frames': m.group('frames'),
                    })
                else:
                    print('re didnt match:', l)
    return data


def get_cs(x): 
    return tuple(int(v, 16) for v in x['frames'].split(' > ')) 
                                                                                                                                                                                                                                                                                 

def are_equal(c1, c2): 
    if len(c1) != len(c2): 
        return False 
    for f1,f2 in zip(c1,c2): 
        if f1 == 0 or f2 == 0: 
            pass 
        else: 
            if (f1 & 0xfff) != (f2 & 0xfff): 
                return False 
    return True 
                                                                                                                                                                                                                                                                                 

def main():
    p = argparse.ArgumentParser()
    p.add_argument('fname')
    p.add_argument('fname2')
    args = p.parse_args()

    data = parse_location_translations(args.fname)
    d2 = parse_location_translations(args.fname2)

    eqs = [(x['idx'] ,y['idx'] , are_equal(get_cs(x), get_cs(y))) for x,y in zip(sorted(data[-1], key=lambda e: e['idx']), sorted(d2[-1], key=lambda e: e['idx']))]
    
    from IPython import embed
    embed()


if __name__ == '__main__':
    main()
