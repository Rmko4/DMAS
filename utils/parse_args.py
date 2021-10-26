import argparse
from utils.comp_range import Range

run_keys = ['T_onset', 'T_record']
save_keys = ['save_filename']

def pop_keys(dict, keys):
    items = {k: dict.pop(k) for k in list(dict.keys()) if k in keys}
    return items

def parse_args(print_args=False):
    parser = argparse.ArgumentParser(description='MAS for trust in exchange')
    parser.add_argument('-a', '--agent-class', dest='AgentClass', default='MSAgent',
                        choices=['MSAgent', 'WHAgent', 'RLAgent', 'GossipAgent'])
    parser.add_argument('-m', '--mobility-rate', default=0.2,
                        type=float, choices=[Range(0.0, 1.0)])
    parser.add_argument('-N', '--number-of-agents', default=1000,
                        type=int, choices=[Range(0, 10000)])
    parser.add_argument('-n', '--neighbourhood-size',
                        default=30, type=int, choices=[Range(0, 10000)])
    parser.add_argument('-l', '--learning-rate', default=0.02,
                        type=float, choices=[Range(0.0, 1.0)], help='Only for RLAgent')
    parser.add_argument('-r', '--relative-reward', default=False,
                        type=bool, choices=[True, False], help='Only for RLAgent')
    parser.add_argument('-t1', '--T_onset', default='100',
                        type=int, choices=[Range(0, int(1e6))])
    parser.add_argument('-t2', '--T_record', default='1000',
                        type=int, choices=[Range(0, int(1e6))])
    parser.add_argument('--save-filename', default='data.csv',
                        help='Saves to /data/SAVE-FILENAME')

    args = parser.parse_args()

    if args.neighbourhood_size > args.number_of_agents:
        raise ValueError('neighbourhood-size is larger than number-of-agents')
    if args.AgentClass != 'RLAgent':
        del args.learning_rate
        del args.relative_reward

    kwargs = vars(args)
    
    run_args = pop_keys(kwargs, run_keys)
    save_filename = pop_keys(kwargs, save_keys)[save_keys[0]]

    if print_args:
        print("Model params: " + str(kwargs))
        print("Run params: " + str(run_args))

    return kwargs, run_args, save_filename