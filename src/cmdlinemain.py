'''
# Copyright 2010 Mandar Vaze (mandarvaze@gmail.com)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
# * Neither the name of the nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

import simplenote as sn
import sys

#TODO : Ask email/password interactively if empty

def main():
    """Important to have strings email and password updated before you login()
    """ 
    email = ''
    password = ''

    try:
        tok = sn.login(email, password)
    except:
        print "Unable to login"
        exit(-1)
    
    try:
        completeList = sn.getIndex(tok,email)
    except:
        print "Unable to get the index"
        exit(-1)

    noteList = [] # Contains only those notes that are not marked for deletion
    c = 1
    for i in completeList:
        if i['deleted'] == False :
            print '[%d] %s' % (c, i['key'])
            c = c + 1
            noteList.append(i)

    print "Which note do you wish to read ?"
    idx = sys.stdin.readline()
    key = noteList[int(idx)-1]['key']

    try:
        note = sn.getNoteFromKey(key,tok,email)
    except:
        print "Unable to get the note from key %s" % key
        exit(-1)

    title = note.readline().decode('utf-8').rstrip()[:40]
    body = note.read().decode('utf-8')
    note.close()
    print title
    print body

if __name__ == '__main__':
    main()