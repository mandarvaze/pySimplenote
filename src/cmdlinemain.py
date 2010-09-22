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
from optparse import OptionParser

#Globals for now - These need to be class variables
email =''
tok =''
noteList = [] # Contains only those notes that are not marked for deletion

def displayNote():
    print "Which note do you wish to read ?"
    idx = sys.stdin.readline()
    key = noteList[int(idx)-1]['key']

#    try:
    note = sn.getNoteFromKey(key,tok,email)
#    except:
#        print "Unable to get the note from key %s" % key
#        exit(-1)

    title = note.readline().decode('utf-8').rstrip()[:40]
    body = note.read().decode('utf-8')
    note.close()
    print title
    print body

def addNote():
    print "Enter the note. Enter only . on new line to stop entering note contents :"
    noteContents = ''
    while 1 :
        n = sys.stdin.readline() #n will have \n at the last 
        if (n.startswith('.') and len(n) == 2) :
            break
        else:
            noteContents = noteContents + n

    sn.addUpdateNote(tok, email, noteContents)

def deleteNote():
    print "Which note do you wish to delete ?"
    idx = sys.stdin.readline()
    key = noteList[int(idx)-1]['key']

    try:
        note = sn.deleteNote(key,tok,email)
    except:
        print "Unable to delete the note from key %s" % key
        exit(-1)


def main():
    global email
    global tok
    global noteList

    parser = OptionParser()
    parser.add_option("-e", "--email", action="store", type="string", dest="email", 
                  help="Email to login to Simplenote (Mandatory)")
    parser.add_option("-p", "--password", action="store", type="string", dest="password", 
                  help="Password to login to Simplenote (Mandatory)")
    parser.add_option("-a", "--add", action="store_true", help="Add a new note. (Enter note interactively)")
    parser.add_option("-d", "--delete", action="store_true",  help="Delete a note")
    parser.add_option("-l", "--list", action="store_true",  help="Display a specific note")
    parser.add_option("-v", "--verbose", action="store_true",  help="Print Extra messages")    
    (options, args) = parser.parse_args()

    if options.verbose:
        print options
    
    # Making sure all mandatory options provided.
    # Thanks : http://www.alexonlinux.com/pythons-optparse-for-human-beings#support_for_mandatory_%28required%29_options.
    mandatories = ['email', 'password']
    for m in mandatories:
        if not options.__dict__[m]:
            print "mandatory option is missing\n"
            parser.print_help()
            exit(-1)

    email = options.email
#TODO: Rather than plain text password on cmdline, implement option to ask interactively without echoing
    password = options.password

    try:
        tok = sn.login(email, password)
    except:
        print "Unable to login"
        exit(-1)

    if options.add:
        addNote()
        exit(0)

    try:
        completeList = sn.getIndex(tok,email)
    except:
        print "Unable to get the index"
        exit(-1)

    c = 1
    for i in completeList:
        if i['deleted'] == False :
            print '[%d] %s' % (c, i['key'])
            c = c + 1
            noteList.append(i)

    if options.verbose:
        print noteList

    if options.list:
        displayNote()
        exit(0)

    if options.delete:
        deleteNote()
        exit(0)

if __name__ == '__main__':
    main()
