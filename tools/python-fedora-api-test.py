import os
import getpass
import logging

from fedora.client import BodhiClient

log = logging.getLogger('fedora.client.bodhi')

build = u'qt-creator-3.4.1-3.fc23'
username = os.getenv('USER')
#username = raw_input('FAS Username: ')
#password = getpass.getpass()
import subprocess
p = subprocess.Popen(['/usr/bin/pass', 'sys/fas'], stdout=subprocess.PIPE)
out, err = p.communicate()
password = out.strip()

print('Logging into bodhi2')
bodhi = BodhiClient(staging=True, username=username, password=password)

print('Logged in! Creating new update...')

result = bodhi.save(
        builds=build,
        type='bugfix',
        notes='The quick brown fox jumped over the lazy dog',
)
print(result)

print('Querying update')
result = bodhi.query(builds='qt-creator-3.4.1-3.fc23')
updates = result['updates']
update = updates[0]
assert len(updates) == 1, len(updates)
assert result['total'] == 1, result
alias = update['alias']
print(alias)

print(bodhi.update_str(update))
print('')
print(bodhi.update_str(update, minimal=True))

#print('Call /latest_builds')
#result = bodhi.latest_builds('kernel')
#print(result)
#
#print('Querying all releases')
#result = bodhi.get_releases()
#print(result)
#
#print('Looking for candidate builds')
#print(bodhi.candidates())
#
#print('Looking for local builds in updates-testing')
#for update in bodhi.testable():
#    print(bodhi.update_str(update))

#print('Querying by release')
#result = bodhi.query(release='F23')
#print(result)
#updates = result['updates']
#print(updates)
#assert len(updates) == 1, len(updates)
#assert result['total'] == 1, result
#assert updates[0].alias == alias
#print('%d updates returned' % len(updates))
#
#print('Querying by release and package')
#result = bodhi.query(package='qt-creator', release='F23')
#updates = result['updates']
#assert len(updates) == 1, len(updates)
#assert result['total'] == 1, result
#assert updates[0]['alias'] == alias
#print('%d updates returned' % len(updates))
#
#print('Querying by release and package and status')
#result = bodhi.query(package='qt-creator', release='F23', status='pending')
#updates = result.updates
#assert len(updates) == 1, len(updates)
#assert result['total'] == 1, result
#assert updates[0]['alias'] == alias
#print('%d updates returned' % len(updates))
#
#print('Querying by release and package and status and limit')
#result = bodhi.query(type='security', limit=2)
#updates = result.updates
#assert len(updates) == 2, len(updates)
#assert updates[0]['type'] == 'security'
#print('%d updates returned' % len(updates))
#
#print('Querying by release with limit (blockerbugs)')
#result = bodhi.query(limit=100, release='F23')
#updates = result['updates']
#assert len(updates) == 1, len(updates)
#assert updates[0]['type'] == 'bugfix', updates[0].type
#print('%d updates returned' % len(updates))

#print('Requesting stable')
#result = bodhi.request(update=alias, request='stable')
#assert result['status'] == 'error', result
#assert len(result['errors']) == 1
#assert result['errors'][0]['name'] == 'request'
#
#print('Requesting testing')
#result = bodhi.request(update=alias, request='testing')
#assert result['update']['request'] == 'testing'
#
#print('Revoking request')
#result = bodhi.request(update=alias, request='revoke')
#assert result['update']['request'] == None

print('Adding comment')
result = bodhi.comment(update=alias, comment='yay', karma=1)
print result
comment = result['comment']
assert comment['author'] == username
assert comment['text'] == u'yay'
assert comment['update']['title'] == build

print('Querying multiple pages of updates')
query = dict(limit=100, release='F22', critpath=True)
result = bodhi.query(**query)
updates = result.updates
total = result.total
page = result.page
pages = result.pages
print('%r pages' % result.pages)
print('%r page' % result.page)
print('%r total' % result.total)
while result.page < result.pages:
    print('Querying page %d out of %d' % (result.page + 1, pages))
    result = bodhi.query(page=result.page + 1, **query)
    updates.extend(result.updates)

print('Fetched %d updates total' % len(updates))
assert len(updates) == total, len(updates)

print('Querying for my updates')
result = bodhi.query(mine=True)
print(result)
assert result.updates[0].user.name == username, result.updates[0].user.name

