# -*- coding: utf-8 -*-

import os
import gzip
from experiment_library import test, zip_file_write, file_write, RESULTS_DIR


TEST_PAGE = 'cleared_youtube'
with open(TEST_PAGE, 'r') as f:
    TOTAL = len(f.read())
with gzip.open(TEST_PAGE + '.gz', 'w') as f:
    with open(TEST_PAGE, 'r') as g:
        total = g.read()
    f.write(total)
with open(TEST_PAGE + '.gz', 'r') as f:
    TOTAL_ZIP = len(f.read())

ORIGIN_LEN = 50
SECRETS_PER_ORIGIN = 1
RATE = 0.01


def general_info(experiment_name, mode):
    info = []
    info.append('=======CTX Benchmark=======\n')
    info.append('Total length: {}'.format(TOTAL))
    info.append('Total zipped length: {}'.format(TOTAL_ZIP))
    info.append('Origins: {}'.format(ORIGIN_LEN))
    info.append('Secrets per origin: {}'.format(SECRETS_PER_ORIGIN))
    info.append('Mode: {}'.format(mode))
    info.append('Rate: {}'.format(RATE))
    info.append('EXPERIMENT: {}'.format(experiment_name))
    info.append('\n')
    return '\n'.join(info)


def experiment_info(identification, total, t, mode, experiment_name):
    with open(os.path.join(RESULTS_DIR, '{}_{}_{}_unprotected_total'.format(mode, identification, experiment_name)), 'r') as f:
        unprotected_total = len(f.read())
    with open(os.path.join(RESULTS_DIR, '{}_{}_{}_total'.format(mode, identification, experiment_name)), 'r') as f:
        protected_total = len(f.read())
    with open(os.path.join(RESULTS_DIR, '{}_{}_{}_unprotected_total.gz'.format(mode, identification, experiment_name)), 'r') as f:
        unprotected_total_zip = len(f.read())
    with open(os.path.join(RESULTS_DIR, '{}_{}_{}_total.gz'.format(mode, identification, experiment_name)), 'r') as f:
        protected_total_zip = len(f.read())
    overhead = '%sOverhead: %.5f | %d' % (
        str(identification) + ' '*(10-len(str(identification))),
        (protected_total-unprotected_total)/float(unprotected_total),
        protected_total-unprotected_total,
    )
    overhead_zip = '%sOverhead zipped: %.5f | %d' % (
        str(identification) + ' '*(10-len(str(identification))),
        (protected_total_zip-unprotected_total_zip)/float(unprotected_total_zip),
        protected_total_zip-unprotected_total_zip
    )
    time = '%stime: %.5f' % (
        str(identification) + ' '*(10-len(str(identification))),
        t
    )
    return {
        'overhead': overhead,
        'overhead_zip': overhead_zip,
        'time': time,
    }

EXPERIMENTS = [
    ('rate', [(0.001*i, 0.001*i, SECRETS_PER_ORIGIN, TOTAL, ORIGIN_LEN) for i in range(1, 50, 1)]),
    ('secret_per_origin', [(i, RATE, i, TOTAL, ORIGIN_LEN) for i in range(1, 50, 1)]),
    ('total', [(TOTAL/i, RATE, SECRETS_PER_ORIGIN, TOTAL/i, ORIGIN_LEN) for i in range(50, 0, -1)]),
    ('origins', [(i, RATE, SECRETS_PER_ORIGIN, TOTAL, i) for i in range(1, 50, 1)]),
]

MODES = [
    'english',
    'printable',
    'random'
]

for mode in MODES:
    for experiment in EXPERIMENTS:
        experiment_name = experiment[0]
        experiment_stats = experiment[1]
        info = ''

        info += general_info(experiment_name, mode)
        overhead = []
        overhead_zip = []
        time = []

        for i in experiment_stats:
            identification = i[0]
            rate = i[1]
            secrets_per_origin = i[2]
            total = i[3]
            origin_len = i[4]

            origins = int(origin_len/secrets_per_origin)
            secret_len = int((rate*total) / (origins*secrets_per_origin))

            with open(TEST_PAGE, 'r') as f:
                cleared = f.read()[:total]

            t, protected, secrets = test(origins, secret_len, secrets_per_origin, mode)

            blueprint = cleared[:-1*len(''.join(secrets))]

            aggr = blueprint + ''.join(secrets)
            unp = len(aggr)
            file_write('{}_{}_{}_unprotected_total'.format(mode, identification, experiment_name), aggr)
            zip_file_write('{}_{}_{}_unprotected_total'.format(mode, identification, experiment_name), aggr)

            aggr = blueprint + ''.join(protected)
            p = len(aggr)
            file_write('{}_{}_{}_total'.format(mode, identification, experiment_name), aggr)
            zip_file_write('{}_{}_{}_total'.format(mode, identification, experiment_name), aggr)

            i = experiment_info(identification, total, t, mode, experiment_name)

            overhead.append(i['overhead'])
            overhead_zip.append(i['overhead_zip'])
            time.append(i['time'])

        info += '\n'.join(overhead)
        info += '\n'
        info += '\n'.join(overhead_zip)
        info += '\n'
        info += '\n'.join(time)

        with open(os.path.join(RESULTS_DIR, '{}_{}_{}_{}_{}_info'.format(experiment_name, TOTAL, mode, ORIGIN_LEN, SECRETS_PER_ORIGIN)), 'w') as f:
            f.write(info)

        print info
