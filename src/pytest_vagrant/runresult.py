# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import fnmatch

from pytest_vagrant.errors import MatchError


class RunResult(object):
    """ Stores the results from running a command
    Attributes:
    :command: The command that was executed
    :cwd: Current working directory i.e. path where the command was executed
    :stdout: The standard output stream generated by the command
    :stderr: The standard error stream generated by the command
    :returncode: The return code set after invoking the command
    """

    def __init__(self, command, cwd, stdout, stderr, returncode):
        """ Create a new RunResult object
        """

        self.command = command
        self.cwd = cwd
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

    def match(self, stdout=None, stderr=None):
        """ Matches the lines in the output with the pattern. The match
        pattern can contain basic wildcards, see
        https://docs.python.org/2/library/fnmatch.html
        For convenience:
            +-----------------------------------------+
            |Pattern|Meaning                          |
            +-----------------------------------------+
            |*      |matches everything               |
            +-----------------------------------------+
            |?      |matches any single character     |
            +-----------------------------------------+
            |[seq]  |matches any character in seq     |
            +-----------------------------------------+
            |[!seq] |matches any character not in seq |
            +-----------------------------------------+
        Simple example:
            out.match('*success*')
        Will return True if one or more of the lines in out.output contains
        the word success.
        :param pattern: Pattern to search for in the list of output string
        :return: True if the pattern is found in one or more of the output
                 lines.
        """
        if [stdout, stderr].count(None) != 1:
            raise TypeError("Exactly 1 of the ways must be used.")

        match = stdout if stdout else stderr
        output = self.stdout if stdout else self.stderr

        match_lines = fnmatch.filter(output.splitlines(), match)
        if not match_lines:
            raise MatchError(match=match, output=output)

    def __str__(self):
        """ Print the RunResult object as a string
        """
        run_string = "RunResult\n" \
                     "command: {command}\n" \
                     "cwd: {cwd}\n" \
                     "returncode: {returncode}\n" \
                     "stdout: \n{stdout}" \
                     "stderr: \n{stderr}"

        return run_string.format(command=self.command, cwd=self.cwd,
                                 returncode=self.returncode,
                                 stdout=self.stdout, stderr=self.stderr)
