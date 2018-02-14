"""explorer functions

Functions to generate ZFSSA explorers.
"""
import os
import csv
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from zipfile import ZipFile
from zfssa_utils.common import (exists, response_size, read_yaml_file,
                                urls_constructor, createprogress, fetch,
                                HEADER, createlogger, EXPLORERLOGFILE)


def trimpath(outputdir, filename):
    """Return only the last part of parent path joined with the filename."""
    # zfssa_explorer_xxx.xxx.xxx.xxx_xxxxxx_xxxxxx/filename
    zipdir = os.path.split(outputdir)[1]
    return os.path.join(zipdir, filename)


def create_csv(data, datatype, outputdir):
    """Create CSV files for data retrieved from zfssa."""
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    if datatype == "version":
        d = data['version']
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(['href', 'nodename', 'mkt_product', 'product',
                             'version', 'install_time', 'update_time',
                             'boot_time', 'asn', 'csn', 'part', 'urn',
                             'navname', 'navagent', 'http', 'ssl',
                             'ak_version', 'os_version', 'bios_version',
                             'sp_version'])
            writer.writerow([d['href'], d['nodename'], d['mkt_product'],
                             d['product'], d['version'], d['install_time'],
                             d['update_time'], d['boot_time'], d['asn'],
                             d['csn'], d['part'], d['urn'], d['navname'],
                             d['navagent'], d['http'], d['ssl'],
                             d['ak_version'], d['os_version'],
                             d['bios_version'], d['sp_version']])
    elif datatype == "cluster":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["state", "description", "peer_asn",
                             "peer_hostname", "peer_state",
                             "peer_description"])
            writer.writerow([data['cluster']['state'],
                             data['cluster']['description'],
                             data['cluster']['peer_asn'],
                             data['cluster']['peer_hostname'],
                             data['cluster']['peer_state'],
                             data['cluster']['peer_description']])
            writer.writerow(["owner", "type", "user_label", "details", "href"])
            for r in data['cluster']['resources']:
                writer.writerow([r['owner'], r['type'], r['user_label'],
                                 r['details'], r['href']])
    elif datatype == "problems":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["uuid", "code", "diagnosed", "phoned_home",
                             "severity", "type", "url", "description",
                             "impact", "response", "action", "href"])
            for d in data['problems']:
                writer.writerow([d['uuid'], d['code'], d['diagnosed'],
                                 d['phoned_home'], d['severity'], d['type'],
                                 d['url'], d['description'], d['impact'],
                                 d['response'], d['action'], d['href']])
    elif datatype == "datalinks":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(['class', 'label', 'mac', 'links', 'pkey',
                             'linkmode', 'mtu', 'id', 'speed', 'duplex',
                             'datalink', 'href'])
            for d in data['datalinks']:
                writer.writerow([d['class'], d['label'], d['mac'], d['links'],
                                 exists(d, 'pkey'), exists(d, 'linkmode'),
                                 exists(d, 'mtu'), exists(d, 'id'),
                                 exists(d, 'speed'), exists(d, 'duplex'),
                                 d['datalink'], d['href']])
    elif datatype == "devices":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(['speed', 'up', 'active', 'media', 'factory_mac',
                             'port', 'guid', 'duplex', 'device', 'href'])
            for d in data['devices']:
                writer.writerow([d['speed'], d['up'], d['active'], d['media'],
                                 d['factory_mac'], exists(d, 'port'),
                                 exists(d, 'guid'), exists(d, 'duplex'),
                                 d['device'], d['href']])
    elif datatype == "interfaces":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(['state', 'curaddrs', 'class', 'label', 'enable',
                             'admin', 'links', 'v4addrs', 'v4dhcp',
                             'v4directnets', 'v6addrs', 'v6dhcp',
                             'v6directnets', 'key', 'standbys', 'interface',
                             'href'])
            for d in data['interfaces']:
                writer.writerow([d['state'], d['curaddrs'], d['class'],
                                 d['label'], d['enable'], d['admin'],
                                 d['links'], d['v4addrs'], d['v4dhcp'],
                                 d['v4directnets'], d['v6addrs'], d['v6dhcp'],
                                 d['v6directnets'], exists(d, 'key'),
                                 exists(d, 'standbys'), d['interface'],
                                 d['href']])
    elif datatype == "routes":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["status", "family", "destination", "mask", "href",
                             "interface", "type", "gateway"])
            for d in data['routes']:
                writer.writerow([d['status'], d['family'], d['destination'],
                                 d['mask'], d['href'], d['interface'],
                                 d['type'], d['gateway']])
    elif datatype == "routing":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["href", "multihoming"])
            writer.writerow([data['routing']['href'],
                             data['routing']['multihoming']])
    elif datatype == "pools":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(['status', 'profile', 'name', 'usage_available',
                             'usage_available (Human)',
                             'usage_usage_snapshots',
                             'usage_usage_snapshots (Human)', 'usage_used',
                             'usage_used (Human)', 'usage_compression',
                             'usage_usage_data', 'usage_usage_data (Human)',
                             'usage_free', 'usage_free (Human)',
                             'usage_dedupratio', 'usage_total',
                             'usage_total (Human)', 'usage_usage_total',
                             'usage_usage_total (Human)', 'peer', 'href',
                             'owner', 'asn'])
            for d in data['pools']:
                if d['status'] == "exported":
                    writer.writerow([d['status'], "-", d['name'], "-", "-",
                                     "-", "-", "-", "-", "-", "-", "-", "-",
                                     "-", "-", "-", "-", "-", "-", d['peer'],
                                     exists(d, 'href'), d['owner'], d['asn']])
                else:
                    u = d['usage']
                    writer.writerow([d['status'], d['profile'], d['name'],
                                     u['available'],
                                     response_size(u['available']),
                                     u['usage_snapshots'],
                                     response_size(u['usage_snapshots']),
                                     u['used'], response_size(u['used']),
                                     u['compression'], u['usage_data'],
                                     response_size(u['usage_data']), u['free'],
                                     response_size(u['free']), u['dedupratio'],
                                     u['total'], response_size(u['total']),
                                     u['usage_total'],
                                     response_size(u['usage_total']),
                                     d['peer'], exists(d, 'href'),
                                     d['owner'], d['asn']])
    elif datatype == "projects":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(['snapdir', 'default_volblocksize',
                             'defaultgroupquota', 'logbias', 'creation',
                             'nodestroy', 'dedup', 'sharenfs', 'href',
                             'sharesmb', 'default_permissions', 'mountpoint',
                             'snaplabel', 'id', 'readonly', 'space_data',
                             'space_data (Human)', 'compression',
                             'defaultuserquota', 'src_snapdir', 'src_logbias',
                             'src_dedup', 'src_sharenfs', 'src_sharesmb',
                             'src_mountpoint', 'src_rrsrc_actions',
                             'src_compression', 'src_sharetftp',
                             'src_encryption', 'src_sharedav', 'src_copies',
                             'src_aclinherit', 'src_shareftp', 'src_readonly',
                             'src_keychangedate', 'src_secondarycache',
                             'src_maxblocksize', 'src_exported', 'src_vscan',
                             'src_reservation', 'src_atime', 'src_recordsize',
                             'src_checksum', 'src_sharesftp', 'src_nbmand',
                             'src_aclmode', 'src_rstchown', 'default_sparse',
                             'encryption', 'aclmode', 'copies', 'aclinherit',
                             'compressratio', 'shareftp', 'canonical_name',
                             'recordsize', 'recordsize (Human)',
                             'keychangedate', 'space_available',
                             'space_available (Human)', 'secondarycache',
                             'name', 'space_snapshots',
                             'space_snapshots (Human)', 'space_unused_res',
                             'space_unused_res (Human)', 'quota',
                             'quota (Human)', 'maxblocksize',
                             'maxblocksize (Human)', 'exported',
                             'default_volsize', 'default_volsize (Human)',
                             'vscan', 'reservation', 'reservation (Human)',
                             'keystatus', 'atime', 'pool', 'default_user',
                             'space_unused_res_shares',
                             'space_unused_res_shares (Human)', 'sharetftp',
                             'checksum', 'space_total', 'space_total (Human)',
                             'default_group', 'sharesftp', 'rstchown',
                             'sharedav', 'nbmand'])
            for d in data['projects']:
                s = d['source']
                writer.writerow([d['snapdir'],
                                 response_size(d['default_volblocksize']),
                                 d['defaultgroupquota'], d['logbias'],
                                 d['creation'], d['nodestroy'], d['dedup'],
                                 d['sharenfs'], d['href'], d['sharesmb'],
                                 d['default_permissions'], d['mountpoint'],
                                 d['snaplabel'], d['id'], d['readonly'],
                                 d['space_data'],
                                 response_size(d['space_data']),
                                 d['compression'], d['defaultuserquota'],
                                 s['snapdir'], s['logbias'], s['dedup'],
                                 s['sharenfs'], s['sharesmb'], s['mountpoint'],
                                 exists(s, 'rrsrc_actions'), s['compression'],
                                 s['sharetftp'], exists(s, 'encryption'),
                                 s['sharedav'], s['copies'], s['aclinherit'],
                                 s['shareftp'], s['readonly'],
                                 s['keychangedate'], s['secondarycache'],
                                 s['maxblocksize'], s['exported'], s['vscan'],
                                 s['reservation'], s['atime'], s['recordsize'],
                                 s['checksum'], s['sharesftp'], s['nbmand'],
                                 s['aclmode'], s['rstchown'],
                                 d['default_sparse'], d['encryption'],
                                 d['aclmode'], d['copies'], d['aclinherit'],
                                 d['compressratio'], d['shareftp'],
                                 d['canonical_name'], d['recordsize'],
                                 response_size(d['recordsize']),
                                 d['keychangedate'], d['space_available'],
                                 response_size(d['space_available']),
                                 d['secondarycache'], d['name'],
                                 d['space_snapshots'],
                                 response_size(d['space_snapshots']),
                                 d['space_unused_res'],
                                 response_size(d['space_unused_res']),
                                 d['quota'], response_size(d['quota']),
                                 d['maxblocksize'],
                                 response_size(d['maxblocksize']),
                                 d['exported'], d['default_volsize'],
                                 response_size(d['default_volsize']),
                                 d['vscan'], d['reservation'],
                                 response_size(d['reservation']),
                                 d['keystatus'], d['atime'], d['pool'],
                                 d['default_user'],
                                 d['space_unused_res_shares'],
                                 response_size(d['space_unused_res_shares']),
                                 d['sharetftp'], d['checksum'],
                                 d['space_total'],
                                 response_size(d['space_total']),
                                 d['default_group'], d['sharesftp'],
                                 d['rstchown'], d['sharedav'], d['nbmand']])
    elif datatype == "luns":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["logbias", "creation", "nodestroy",
                             "assignednumber", "copies", "href", "fixednumber",
                             "space_data", "space_data (Human)", "id",
                             "writecache", "compression", "encryption",
                             "dedup", "snaplabel", "compressratio",
                             "src_compression", "src_encryption",
                             "src_logbias", "src_dedup", "src_copies",
                             "src_maxblocksize", "src_exported",
                             "src_checksum", "src_keychangedate",
                             "src_rrsrc_actions", "src_secondarycache",
                             "space_total", "space_total (Human)", "lunumber",
                             "keychangedate", "space_available",
                             "space_available (Human)", "secondary_cache",
                             "status", "space_snapshots",
                             "space_snapshots (Human)", "lunguid",
                             "maxblocksize", "maxblocksize (Human)",
                             "exported", "initiatorgroup", "volsize",
                             "volsize (Human)", "keystatus", "pool",
                             "volblocksize", "volblocksize (Human)",
                             "writelimit", "name", "checksum",
                             "canonical_name", "project", "sparse",
                             "targetgroup", "effectivewritelimit"])
            for d in data['luns']:
                s = d['source']
                writer.writerow([d['logbias'], d['creation'], d['nodestroy'],
                                 d['assignednumber'], d['copies'], d['href'],
                                 d['fixednumber'], d['space_data'],
                                 response_size(d['space_data']), d['id'],
                                 d['writecache'], d['compression'],
                                 d['encryption'], d['dedup'], d['snaplabel'],
                                 d['compressratio'], s['compression'],
                                 exists(s, 'encryption'), s['logbias'],
                                 s['dedup'], s['copies'], s['maxblocksize'],
                                 s['exported'], s['checksum'],
                                 s['keychangedate'],
                                 exists(s, 'rrsrc_actions'),
                                 s['secondarycache'], d['space_total'],
                                 response_size(d['space_total']),
                                 d['lunumber'], d['keychangedate'],
                                 d['space_available'],
                                 response_size(d['space_available']),
                                 d['secondarycache'], d['status'],
                                 d['space_snapshots'],
                                 response_size(d['space_snapshots']),
                                 d['lunguid'], d['maxblocksize'],
                                 response_size(d['maxblocksize']),
                                 d['exported'], d['initiatorgroup'],
                                 d['volsize'], response_size(d['volsize']),
                                 d['keystatus'], d['pool'], d['volblocksize'],
                                 response_size(d['volblocksize']),
                                 exists(d, 'writelimit'), d['name'],
                                 d['checksum'], d['canonical_name'],
                                 d['project'], d['sparse'], d['targetgroup'],
                                 exists(d, 'effectivewritelimit')])
    elif datatype == "filesystems":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["snapdir", "logbias", "creation", "nodestroy",
                             "dedup", "sharenfs", "sharesmb_abe", "sharesmb",
                             "root_acl", "mountpoint", "casesensitivity",
                             "snaplabel", "id", "readonly", "sharesmb_name",
                             "space_data", "space_data (Human)", "compression",
                             "sharetftp", "src_snapdir", "src_logbias",
                             "src_dedup", "src_sharenfs", "src_sharesmb",
                             "src_mountpoint", "src_rrsrc_actions",
                             "src_compression", "src_sharetftp",
                             "src_encryption", "src_sharedav", "src_copies",
                             "src_aclinherit", "src_shareftp", "src_readonly",
                             "src_keychangedate", "src_secondarycache",
                             "src_maxblocksize", "src_exported", "src_vscan",
                             "src_reservation", "src_atime", "src_recordsize",
                             "src_checksum", "src_sharesftp", "src_nbmand",
                             "src_aclmode", "src_rstchown", "encryption",
                             "aclmode", "copies", "smbshareacl", "aclinherit",
                             "compressratio", "shareftp", "canonical_name",
                             "recordsize", "recordsize (Human)",
                             "keychangedate", "space_available",
                             "space_available (Human)", "root_group",
                             "secondarycache", "root_user", "root_permissions",
                             "shadow", "space_snapshots",
                             "space_snapshots (Human)", "href",
                             "space_unused_res", "space_unused_res (Human)",
                             "quota", "quota (Human)", "utf8only",
                             "sharesmb_dfsroot", "maxblocksize",
                             "maxblocksize (Human)", "exported", "vscan",
                             "reservation", "reservation (Human)", "keystatus",
                             "atime", "pool", "quota_snap",
                             "quota_snap (Human)", "space_unused_res_shares",
                             "name", "checksum", "space_total",
                             "space_total (Human)", "project", "normalization",
                             "sharesftp", "rstchown", "reservation_snap",
                             "reservation_snap (Human)", "sharedav", "nbmand"])
            for d in data['filesystems']:
                s = d['source']
                writer.writerow([d['snapdir'], d['logbias'], d['creation'],
                                 d['nodestroy'], d['dedup'], d['sharenfs'],
                                 exists(d, 'sharesmb_abe'), d['sharesmb'],
                                 exists(d, 'root_acl'), d['mountpoint'],
                                 d['casesensitivity'], d['snaplabel'], d['id'],
                                 d['readonly'], exists(d, 'sharesmb_name'),
                                 d['space_data'],
                                 response_size(d['space_data']),
                                 d['compression'], d['sharetftp'],
                                 s['snapdir'], s['logbias'], s['dedup'],
                                 s['sharenfs'], s['sharesmb'], s['mountpoint'],
                                 exists(s, 'rrsrc_actions'), s['compression'],
                                 s['sharetftp'], exists(s, 'encryption'),
                                 s['sharedav'], s['copies'], s['aclinherit'],
                                 s['shareftp'], s['readonly'],
                                 s['keychangedate'], s['secondarycache'],
                                 s['maxblocksize'], s['exported'], s['vscan'],
                                 s['reservation'], s['atime'], s['recordsize'],
                                 s['checksum'], s['sharesftp'], s['nbmand'],
                                 s['aclmode'], s['rstchown'], d['encryption'],
                                 d['aclmode'], d['copies'],
                                 exists(d, 'smbshareacl'), d['aclinherit'],
                                 d['compressratio'], d['shareftp'],
                                 d['canonical_name'], d['recordsize'],
                                 response_size(d['recordsize']),
                                 d['keychangedate'], d['space_available'],
                                 response_size(d['space_available']),
                                 d['root_group'], d['secondarycache'],
                                 d['root_user'], d['root_permissions'],
                                 d['shadow'], d['space_snapshots'],
                                 response_size(d['space_snapshots']),
                                 d['href'], d['space_unused_res'],
                                 response_size(d['space_unused_res']),
                                 d['quota'], response_size(d['quota']),
                                 d['utf8only'], exists(d, 'sharesmb_dfsroot'),
                                 d['maxblocksize'],
                                 response_size(d['maxblocksize']),
                                 d['exported'], d['vscan'], d['reservation'],
                                 response_size(d['reservation']),
                                 d['keystatus'], d['atime'], d['pool'],
                                 d['quota_snap'],
                                 response_size(d['quota_snap']),
                                 exists(d, 'space_unused_res_shares'),
                                 d['name'], d['checksum'], d['space_total'],
                                 response_size(d['space_total']), d['project'],
                                 d['normalization'], d['sharesftp'],
                                 d['rstchown'], d['reservation_snap'],
                                 response_size(d['reservation_snap']),
                                 d['sharedav'], d['nbmand']])
    elif datatype == "fc_initiators":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["alias", "initiator", "href"])
            for d in data['initiators']:
                writer.writerow([d['alias'], d['initiator'], d['href']])
    elif datatype == "fc_initiator-groups":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["name", "initiators", "href"])
            for d in data['groups']:
                writer.writerow([d['name'], d['initiators'], d['href']])
    elif datatype == "fc_targets":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["wwn", "port", "mode", "speed",
                             "discovered_ports", "link_failure_count",
                             "loss_of_sync_count", "loss_of_signal_count",
                             "protocol_error_count", "invalid_tx_word_count",
                             "invalid_crc_count", "href"])
            for d in data['targets']:
                writer.writerow([d['wwn'], d['port'], d['mode'], d['speed'],
                                 d['discovered_ports'],
                                 d['link_failure_count'],
                                 d['loss_of_sync_count'],
                                 d['loss_of_signal_count'],
                                 d['protocol_error_count'],
                                 d['invalid_tx_word_count'],
                                 d['invalid_crc_count'], d['href']])
    elif datatype == "fc_target-groups":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["name", "targets", "href"])
            for d in data['groups']:
                writer.writerow([exists(d, 'name'), exists(d, 'targets'),
                                 exists(d, 'href')])
    elif datatype == "iscsi_initiators":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["alias", "initiator", "chapuser", "chapsecret",
                             "href"])
            for d in data['initiators']:
                writer.writerow([exists(d, 'alias'), exists(d, 'initiator'),
                                 exists(d, 'chapuser'),
                                 exists(d, 'chapsecret'), exists(d, 'href')])
    elif datatype == "iscsi_initiator-groups":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["name", "initiators", "href"])
            for d in data['groups']:
                writer.writerow([exists(d, 'name'), exists(d, 'initiators'),
                                 exists(d, 'href')])
    elif datatype == "iscsi_targets":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["alias", "iqn", "auth", "targetchapuser",
                             "targetchapsecret", "interfaces", "href"])
            for d in data['targets']:
                writer.writerow([exists(d, 'alias'), exists(d, 'iqn'),
                                 exists(d, 'auth'),
                                 exists(d, 'targetchapuser'),
                                 exists(d, 'targetchapsecret'),
                                 exists(d, 'interfaces'), exists(d, 'href')])
    elif datatype == "iscsi_target-groups":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["name", "targets", "href"])
            for d in data['groups']:
                writer.writerow([exists(d, 'name'), exists(d, 'targets'),
                                 exists(d, 'href')])
    elif datatype == "users":
        with open(os.path.join(outputdir, '{}.csv'.format(datatype)),
                  'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["sep=;"])
            writer.writerow(["logname", "type", "uid", "fullname",
                             "initial_password", "require_annotation",
                             "roles", "kiosk_mode", "kiosk_screen", "href"])
            for d in data['users']:
                writer.writerow([d['logname'], d['type'], d['uid'],
                                 d['fullname'], d['initial_password'],
                                 d['require_annotation'], exists(d, 'roles'),
                                 exists(d, 'kiosk_mode'),
                                 exists(d, 'kiosk_screen'), d['href']])


def run_explorer(args):
    """Run explorer from given configfile and create a zip file with all csv
    files generated."""
    configfile = args.server
    config = read_yaml_file(configfile)
    zfsip = "https://{}:215/api".format(config['ip'])
    zauth = (config['username'], config['password'])
    outputdir = os.path.join("data", "zfssa_explorer_{}_{}"
                             .format(config['ip'],
                                     datetime.now().strftime("%d%m%y_%H%M%S")))
    group = urls_constructor(zfsip)

    progbar = None
    initial = 0
    timeout = args.timeout
    verify = args.cert
    if args.progress:
        progbar = createprogress(len(group))
        logger = createlogger(EXPLORERLOGFILE)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {}
        for i in group:
            url = i[0]
            future = executor.submit(fetch, url, zauth, HEADER,
                                     timeout, i[1], verify)
            futures[future] = url

        for future in as_completed(futures):
            url = futures[future]
            try:
                data, datatype = future.result()
            except Exception as exc:
                if progbar:
                    logger.warning('"%s" - "%s"', url, exc)
                    initial += 1
                    progbar.update(initial)
                else:
                    print(exc)
            else:
                if progbar:
                    create_csv(data, datatype, outputdir)
                    logger.info("Collecting '%s' for '%s'", datatype,
                                outputdir)
                    initial += 1
                    progbar.update(initial)
                else:
                    print("++++ Creating csv for {} ++++".format(datatype))
                    create_csv(data, datatype, outputdir)
        try:
            with ZipFile('{}.zip'.format(outputdir), 'w') as outzip:
                for root, _, files in os.walk(outputdir):
                    for file in files:
                        outzip.write(os.path.join(root, file),
                                     trimpath(outputdir, file))
                        os.remove(os.path.join(root, file))
        except FileNotFoundError as err:
            print("Nothing to compress: {}".format(err))
        try:
            os.rmdir(outputdir)
        except FileNotFoundError as err:
            print("Nothing to remove: {}".format(err))
        if progbar:
            progbar.finish()
