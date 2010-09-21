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

from urllib import urlopen
from base64 import b64encode
import json as simplejson


def login(emailid,passwd):
    if len(emailid) == 0 :
        print 'email is empty.'
        raise Exception
    
    if len(passwd) == 0 :
        print 'password is empty.'
        raise Exception

    loginURL = 'https://simple-note.appspot.com/api/login'
    creds = b64encode('email=%s&password=%s' % (emailid, passwd))
    loginurl = urlopen(loginURL, creds)
    token = loginurl.readline().rstrip()
    loginurl.close()
    return token


def getIndex(token,emailid, debug=False):
    """It is important to have logged in before you call getIndex() 
    token is returned when you login
    """

    indexURL = 'https://simple-note.appspot.com/api/index?auth=%s&email=%s' % (token, emailid)
    index = urlopen(indexURL)
    noteList = simplejson.load(index)
    if debug:
        print "indexURL=%s\n" % indexURL
        print noteList
    return noteList

def getNoteFromKey(key,token,emailid, debug=False):
    """It is important to have logged in before you call getNoteFromKey()
    getIndex() would return the list of all the notes, which contains the key
    along with other note data.
    token is returned when you login
    """

    noteURL = 'https://simple-note.appspot.com/api/note?key=%s&auth=%s&email=%s' % (key, token, emailid)
    if debug:
        print "noteURL=%s" % noteURL

    note = urlopen(noteURL)
    return note

def deleteNote(key,token,emailid,dead=0, debug=False):
    """It is important to have logged in before you call deleteNote()
    getIndex() would return the list of all the notes, which contains the key
    along with other note data.
    token is returned when you login
    Set optional parameter "dead" to 1, if you wish to delete the note
    permanantely.
    """
    if dead:
        deleteNoteURL = 'https://simple-note.appspot.com/api/delete?key=%s&auth=%s&email=%s&dead=1' % (key, token, emailid)
    else:
        deleteNoteURL = 'https://simple-note.appspot.com/api/delete?key=%s&auth=%s&email=%s' % (key, token, emailid)

    if debug:
        print "deleteNoteURL=%s" % deleteNoteURL
    delURL = urlopen(deleteNoteURL)
    print delURL.getcode()
    delURL.close()
