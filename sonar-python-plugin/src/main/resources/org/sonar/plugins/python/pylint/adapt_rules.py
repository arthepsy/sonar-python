#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   The MIT License (MIT)
   
   Copyright (C) 2014 Andris Raugulis (moo@arthepsy.eu)
   
   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:
   
   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.
   
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
"""
from __future__ import print_function
from cStringIO import StringIO
from lxml import etree
import sys, re, os

pylint_rules = {
	'_long_': ["C0102", "C0103", "C0111", "C0112", "C0121", "C0202", "C0203", "C0301",
	           "C0302", "C0321", "C0322", "C0323", "C0324", "E0001", "E0011", "E0012",
	           "E0100", "E0101", "E0102", "E0103", "E0104", "E0105", "E0106", "E0202",
	           "E0203", "E0211", "E0213", "E0221", "E0222", "E0501", "E0502", "E0503",
	           "E0601", "E0602", "E0611", "E0701", "E0702", "E1001", "E1002", "E1003",
	           "E1101", "E1102", "E1103", "E1111", "F0001", "F0002", "F0003", "F0004",
	           "F0202", "F0220", "F0321", "F0401", "I0001", "I0010", "I0011", "I0012",
	           "I0013", "R0201", "R0401", "R0801", "R0901", "R0902", "R0903", "R0904",
	           "R0911", "R0912", "R0913", "R0914", "R0915", "R0921", "R0922", "R0923",
	           "W0121", "W0101", "W0102", "W0104", "W0105", "W0106", "W0107", "W0122",
	           "W0141", "W0142", "W0201", "W0211", "W0212", "W0221", "W0222", "W0223",
	           "W0231", "W0232", "W0233", "W0311", "W0312", "W0331", "W0332", "W0333",
	           "W0401", "W0402", "W0403", "W0404", "W0406", "W0410", "W0511", "W0601",
	           "W0602", "W0603", "W0604", "W0611", "W0612", "W0613", "W0614", "W0621",
	           "W0622", "W0631", "W0701", "W0702", "W0703", "W0704", "W1001", "W1111"],
	'0.15.2': ["E0710", "W0710"], 
	'0.17.0': ["W0301", "W0108"],
	'0.19.0': ["E0107", "E1120", "E1121", "E1122", "E1123", "E1124", "W0109"], 
	'0.20.0': ["E0711", "W0150", "W0199"],
	'0.23.0': ["F0010"],
	'0.24.0': ["E1200", "E1201", "E1205", "E1206", "E1300", "E1301", "E1302", "E1303", 
	           "E1304", "E1305", "E1306", "W1201", "W1300", "W1301"],
	'0.25.1': ["W0623"],
	'0.26.0': ["C0204", "E0603", "W0711", "W1401", "W1402"],
	'0.27.0': ["E0604", "W0110", "I0020", "I0021", ],
	'0.28.0': ["E0108", "E1310", "W0120"],
	'1.0.0':  ["C0303", "C0304", "C1001", "E1004", "E1125", "W0512", "W0632", "W0712", 
	           "W1501"],
	'1.1.0':  ["C0325", "C0326", "E0235", "E0712", "W0234", "W0633", "I0022"],
	'1.2.0':  ["E0109", "E0110", "E0111", "E0236", "E0238", "W0123"],
	'1.3.0':  ["C0330", "E0237", "E1126", "E1127", "W0640", "W1302", "W1303", "W1304", 
	           "W1305", "W1306", "W1307"],
	'1.4.0':  ["C0327", "C0328", "C0401", "C0402", "E0239", "E1601", "E1602", "E1603", 
	           "E1604", "E1605", "E1606", "E1607", "E1608", "W1202", "W1502", "W1601",
	           "W1602", "W1603", "W1604", "W1605", "W1606", "W1607", "W1608", "W1609",
	           "W1610", "W1611", "W1612", "W1613", "W1614", "W1615", "W1616", "W1617",
	           "W1618", "W1619", "W1620", "W1621", "W1622", "W1623", "W1624", "W1625",
	           "W1626", "W1627", "W1628", "W1629", "W1630", "W1631"]
}

pylint_deprecated = {
	'C0301': 'rule:python:LineLength',
	'C0321': 'rule:python:OneStatementPerLine',
	'C0322': ['1.0.0', 'rule:Pylint:C0326'],
	'C0323': ['1.0.0', 'rule:Pylint:C0326'],
	'C0324': ['1.0.0', 'rule:Pylint:C0326'],
	'E0107': 'rule:python:PreIncrementDecrement',
	'E0501': ['0.23.0', 'rule:Pylint:E0001'],
	'E0502': ['0.23.0', 'rule:Pylint:E0001'],
	'E0503': ['0.22.0', 'rule:Pylint:E0001'],
	'E1103': ['1.4.0', 'rule:Pylint:E1101'],
	'E1122': ['1.4.0'],
	'F0004': ['1.2.0'],
	'F0321': ['0.23.0'],
	'R0912': 'rule:python:FunctionComplexity',
	'W0122': 'rule:python:ExecStatementUsage',
	'W0331': 'rule:python:InequalityUsage',
	'W0333': 'rule:python:BackticksUsage',
	'W0701': ['1.4.0', 'rule:Pylint:W1625'],
	'W0121': ['1.4.0', 'rule:Pylint:E1604'],
	'W0712': ['1.4.0', 'rule:Pylint:E1603'],
	'W1401': 'rule:python:S1717',
}

pylint_rule_priority = {
	'MAJOR': ['E0001', 'E0011', 'E0012', 
	          'E0100', 'E0101', 'E0102', 'E0103', 'E0104', 'E0105', 'E0106', 'E0107', 
	          'E0202', 'E0203', 'E0211', 'E0213', 'E0221', 'E0222', 
	          'E0501', 'E0502', 'E0503', 'E0601', 'E0602', 'E0611', 
	          'E0701', 'E0702', 'E0710', 'E0711', 
	          'E1001', 'E1002', 'E1003', 
	          'E1101', 'E1102', 'E1103', 'E1111', 
	          'E1120', 'E1121', 'E1122', 'E1123', 'E1124', 
	          'E1300', 'E1301', 'E1302', 'E1303', 'E1304', 'E1305', 'E1306', 
	          'F0001', 'F0002', 'F0003', 'F0004', 'F0010', 
	          'F0202', 'F0220', 'F0321', 'F0401', 
	          'E1200', 'E1201', 'E1205', 'E1206']
}

def get_rule_name_builtin(f):
	return 'Referencing built-in %s function' % f
def get_rule_name_method_def(m):
	return 'Definition of method %s' % m

pylint_rule_names = {
	'E0001': 'Syntax error',
	'E0102': 'Redefined function/class/method',
	'E0103': 'Usage of \'break\' or \'continue\' outside of a loop',
	'E0107': 'Use of a non-existent operator',
	'E0202': 'Method hidden by attribute of super class',
	'E0203': 'Access to member before its definition',
	'E0221': 'Implemented interface must be a class',
	'E0611': 'Undefined name',
	'E0702': 'Raising only allowed for classes, instances or strings',
	'E1003': 'Bad first argument given to super',
	'E1101': 'Access of nonexistent member',
	'E1102': 'Calling of not callable',
	'E1120': 'Too few arguments',
	'E1121': 'Too many positional arguments for function call',
	'E1123': 'Passing unexpected keyword argument in function call',
	'E1124': 'Multiple values passed for parameter in function call',
	'E1300': 'Unsupported format character',
	'F0001': 'Analysis failed',
	'F0002': 'Internal pylint error',
	'F0003': 'Ignored builtin module',
	'F0010': 'Error while code parsing',
	'F0220': 'Failed to resolve interfaces',
	'F0401': 'Unable to import module',
	'I0011': 'Locally disabling message',
	'I0012': 'Locally enabling message',
	'R0801': 'Similar lines',
	'R0922': 'Abstract class used too few times',
	'W0122': 'Use of the exec statement',
	'W0141': 'Used black listed builtin function',
	'W0150': 'Statement in finally block may swallow exception',
	'W0199': 'Assert called on a 2-uple',
	'W0211': 'Static method with "self" or "cls" as first argument',
	'W0221': 'Arguments number discrepancy',
	'W0222': 'Signature discrepancy',
	'W0223': 'Abstract method is not overridden',
	'W0311': 'Bad indentation',
	'W0312': 'Mixed tabs/spaces indentation',
	'W0403': 'Relative import',
	'W0404': 'Reimport',
	'W0406': 'Module imports itself',
	'W0511': 'Task marker found',
	'W0602': 'Unassigned global variable',
	'W0611': 'Unused import',
	'W0621': 'Redefining name from outer scope',
	'E1200': 'Unsupported logging format character',
	'C0204': 'Metaclass class method first argument',
	'C0325': 'Unnecessary parentheses',
	'C0326': 'Wrong number of spaces',
	'C0330': 'Bad continuation',
	'C1001': 'Old-style class defined',
	'E0712': 'Avoid catching an exception which doesn\'t inherit from BaseException',
	'E1310': 'Suspicious argument',
	'W0512': 'Source line cannot be decoded using the specified source file encoding',
	'W0623': 'Redefining name in exception handler',
	'W0632': 'Possible unbalanced tuple unpacking',
	'W1401': 'Anomalous backslash escape',
	'W1402': 'Anomalous Unicode escape in byte string',
	'W1501': 'Invalid mode for open',
	
	'C0328': 'Unexpected line ending format',
	'E0239': 'Inheriting from non-class',
	'E1601': 'Use of print statement',
	'I0020': 'Suppressed line',
	'I0021': 'Useless suppression',
	'I0022': 'Deprecated pragma',
	'W1305': 'Mixed format string field numbering',
	'W1601': get_rule_name_builtin('apply'),
	'W1602': get_rule_name_builtin('basestring'),
	'W1603': get_rule_name_builtin('buffer'),
	'W1604': get_rule_name_builtin('cmp function'),
	'W1605': get_rule_name_builtin('coerce function'),
	'W1606': get_rule_name_builtin('execfile function'),
	'W1607': get_rule_name_builtin('file function'),
	'W1608': get_rule_name_builtin('long function'),
	'W1609': get_rule_name_builtin('raw_input function'),
	'W1610': get_rule_name_builtin('reduce function'),
	'W1611': get_rule_name_builtin('StandardError'),
	'W1612': get_rule_name_builtin('unicode'),
	'W1613': get_rule_name_builtin('xrange'),
	'W1614': get_rule_name_builtin('__coerce__'),
	'W1615': get_rule_name_builtin('__delslice__'),
	'W1616': get_rule_name_builtin('__getslice__'),
	'W1617': get_rule_name_builtin('__setslice__'),
	'W1618': 'Missing import from __future__',
	'W1619': 'Division without __future__ statement',
	'W1626': 'Referencing built-in reload function',
	'W1627': get_rule_name_method_def('__oct__'),
	'W1628': get_rule_name_method_def('__hex__'),
	'W1629': get_rule_name_method_def('__nonzero__'),
	'W1630': get_rule_name_method_def('__cmp__'),
	'W1631': 'Usage of function map as implicitly evaluated call'
}

pylint_rules_descr = {
	'C0330': 'Used when continued lines are badly indented.'
}

pylint_missing_rules = {
	'C0322': ['C0321', 'Operator not preceded by a space', 'Used when one of the following operator (!= | <= | == | >= | < | > | = | \+= |-= | \*= | /= | %) is not preceded by a space.'],
	'C0323': ['C0322', 'Operator not followed by a space', 'Used when one of the following operator (!= | <= | == | >= | < | > | = | \+= |-= | \*= | /= | %) is not followed by a space.'],
	'C0324': ['C0323', 'Comma not followed by a space', 'Used when a comma (",") is not followed by a space.'],
	'E0501': ['E0222', 'Non ascii characters found but no encoding specified (PEP 263)', 'Used when some non ascii characters are detected but no encoding is specified, as stated in the PEP 263.'],
	'E0502': ['E0501', 'Wrong encoding specified', 'Used when a known encoding is specified but the file doesn\'t seem to be actually in this encoding.'],
	'E0503': ['E0502', 'Unknown encoding specified', 'Used when an encoding is specified, but it\'s unknown to Python.'],
	'E1103': ['E1102', 'Accessing nonexistent member (type information incomplete)', 'Used when a variable is accessed for an nonexistent member, but Pylint was not able to interpret all possible types of this variable.'],
	'E1122': ['E1121', 'Duplicate keyword argument in function call', 'Used when a function call passes the same keyword argument multiple times.'],
	'E1125': ['E1124', 'Missing mandatory keyword argument', 'Used when a function call does not pass a mandatory keyword-only argument.'],
	'F0004': ['F0003', 'Unexpected inferred value', 'Used to indicate that some value of an unexpected type has been inferred.'],
	'F0321': ['F0220', 'Format detection error', 'Used when an unexpected error occurred in bad format detection. Please report the error if it occurs.'],
	'W0121': ['W0120', 'Use raise ErrorClass(args) instead of raise ErrorClass, args.', 'Used when the alternate raise syntax \'raise foo, bar\' is used instead of \'raise foo(bar)\'.\nThis message can\'t be emitted when using Python >= 3.0.'],
	'W0331': ['W0312', 'Use of the <> operator', 'Used when the deprecated "<>" operator is used instead of "!=".'],
	'W0333': ['W0332', 'Use of the `` operator', 'Used when the deprecated "``" (backtick) operator is used instead of the str() function.'],
	'W0701': ['W0631', 'Raising a string exception', 'Used when a string exception is raised.'],
	'W0712': ['W0711', 'Implicit unpacking of exceptions is not supported in Python 3', 'Python3 will not allow implicit unpacking of exceptions in except clauses.\nSee http://www.python.org/dev/peps/pep-3110/ This message can\'t be emitted whenusing Python >= 3.0.'], 
}

pylint_rule_order_1 = [
	"C0102","C0103","C0111","C0112","C0121","C0202","C0203","C0301","C0302","C0321", 
	"C0322","C0323","C0324","E0001","E0011","E0012","E0100","E0101","E0102","E0103",
	"E0104","E0105","E0106","E0107","E0202","E0203","E0211","E0213","E0221","E0222",
	"E0501","E0502","E0503","E0601","E0602","E0611","E0701","E0702","E0710","E0711",
	"E1001","E1002","E1003","E1101","E1102","E1103","E1111","E1120","E1121","E1122",
	"E1123","E1124","E1300","E1301","E1302","E1303","E1304","E1305","E1306","F0001",
	"F0002","F0003","F0004","F0010","F0202","F0220","F0321","F0401","I0001","I0010",
	"I0011","I0012","I0013","R0201","R0401","R0801","R0901","R0902","R0903","R0904",
	"R0911","R0912","R0913","R0914","R0915","R0921","R0922","R0923","W0101","W0102",
	"W0104","W0105","W0106","W0107","W0108","W0109","W0122","W0141","W0142","W0150",
	"W0199","W0201","W0211","W0212","W0221","W0222","W0223","W0231","W0232","W0233",
	"W0301","W0311","W0312","W0331","W0332","W0333","W0401","W0402","W0403","W0404",
	"W0406","W0410","W0511","W0601","W0602","W0603","W0604","W0611","W0612","W0613",
	"W0614","W0621","W0622","W0631","W0701","W0702","W0703","W0704","W0710","W1001",
	"W1111","W1201","W1300","W1301"]
pylint_rule_order_2 = ["E1200","E1201","E1205","E1206"]
pylint_rule_order_3 = [
	"C0204","C0303","C0304","C0325","C0326","C0330","C1001", "E0108","E0109","E0111",
	"E0235","E0236","E0238","E0603","E0604","E0712","E1004", "E1310","W0110","W0120",
	"W0121","W0123","W0234","W0512","W0623","W0632","W0633", "W0711","W0712","W1401", 
	"W1402","W1501"]

def _err(*objs):
	print(*objs, file=sys.stderr)
	sys.exit(1)

def _out(*objs):
	print(*objs, file=sys.stdout)

def get_rule_key(xrule):
	xrule_key = xrule.find('key')
	return xrule_key.text if xrule_key is not None else None
	
def get_clean_desc_txt(desc):
	desc = re.sub('(<p>)+', '<p>', desc)
	desc = re.sub('(</p>)+', '</p>', desc)
	desc = desc.replace('<p>', '')
	desc = desc.replace('</p>', '\n')
	desc = re.sub('(\n)+', '\n', desc)
	desc = desc.strip()
	lines = []
	for line in desc.split('\n'):
		line = line.strip()
		if len(line) == 0: 
			continue
		add_lines = []
		mxall = re.findall(r'^(.*\.)?([^\.]+http[s]?://[^ ]*)( [^.]+\.)?$', line)
		if len(mxall) > 0:
			for mx in mxall:
				if len(mx[0].strip()) > 0:
					add_lines.append([mx[0], True])
				add_lines.append([mx[1].lstrip() + mx[2], len(mx[2].strip()) > 0])
		else:
			add_lines.append([line, True])
		for vline in add_lines:
			(line, add_dot) = vline
			line = line.rstrip('.')
			if add_dot:
				if not re.search('[!?,]+$', line):
					line = line + '.'
			lines.append(line)
	return '\n'.join(lines)
	
def update_node_text(xnode, text, with_paragraphs = False):
	text = text.strip()
	if with_paragraphs:
		text = '<p>' +  text.replace('\n', '</p>\n<p>') + '</p>'
	xnode.text = etree.CDATA(text)

def get_rule_version(xrule):
	rule_version_found = False
	rule_version = None
	rule_key = get_rule_key(xrule)
	for ver, ver_rules in pylint_rules.items():
		if rule_key in ver_rules:
			rule_version_found = True
			if ver == '_long_': 
				break
			rule_version = ver
	if not rule_version_found:
		_err('rule version not found: ' + rule_key)
	return rule_version

def update_rule_priortiy(xrule):
	xprio = etree.SubElement(xrule, 'priority')
	if xprio is None:
		xprio = etree.SubElement(xrule, 'priority')
	rule_key = get_rule_key(xrule)
	if rule_key.startswith('I'):
		xprio.text = 'INFO'
	elif rule_key in pylint_rule_priority['MAJOR']:
		xprio.text = 'MAJOR'
	else:
		xprio.text = 'MINOR'
	return xprio

def get_rule_name(xrule):
	xname = xrule.find('name')
	if xname is None:
		xname = etree.SubElement(xrule, 'name')
		xname.text = get_rule_version(xrule)
	return xname

def get_rule_desc(xrule):
	xdesc = xrule.find('description')
	if xdesc is None:
		xdesc = etree.SubElement(xrule, 'description')
		xdesc.text = etree.CDATA(get_rule_name(xrule).text)
	return xdesc

def get_fixed_text(text):
	for r in [' \(%s\s*/\s*%s\)', ' \(%s\)', ', not %s', ' "%s"', ' \'%s\'', ' %s', ' %r', '%s']:
		text = re.sub(r, '', text)
	
	replaces = {' , ': ', ',
	            ' !': '!',
	            'datetetime.': 'datetime.', 
	            'unexistent': 'nonexistent',
	            'occured': 'occurred',
	            'whenusing': 'when using', 
	            'more than on ': 'more than one ',
	            'name hide a name': 'name hides a name',
	            'int detect the use': 'int detects the use',
	            'int just try to': 'int just tries to',
	            'conWtains': 'contains',
	             ' (function for Python 3),': ',',
	             'function(Python': 'function (Python',
	             '`(Python': '` (Python',
	            '``from': '`from',
	            'division``': 'division`',
	            'PyLint': 'Pylint'}
	for k, v in replaces.items():
		text = text.replace(k, v)
	
	for mx in re.finditer(r'([a-zA-Z]+)\.([a-zA-Z]+)', text):
		if mx is not None:
			if mx.group(0) in ['e.g', 'i.e']:
				continue
			elif mx.group(1) in ['dict']:
				continue
			elif mx.group(0) in ['ast.literal', 'abc.ABCMeta', 'datetime.time', 'exception.args', 'imp.reload', 'importlib.reload', 'string.format']:
				continue
			elif mx.group(2) in ['html', 'python']:
				continue
			else:
				text = text.replace(mx.group(0), mx.group(1) + '. ' + mx.group(2))
	return text

def update_rule_name(xrule):
	xname = get_rule_name(xrule)
	rule_key = get_rule_key(xrule)
	if rule_key in pylint_rule_names:
		text = pylint_rule_names[rule_key]
	else:
		text = xname.text
		mcs = 'mcs' if rule_key != 'C0202' else 'cls'
		text = re.sub(r'should have %s', 'should have "' + mcs +'"' , text)
		text = get_fixed_text(text)
	update_node_text(xname, text.rstrip(':.'))

def update_rule_description(xrule):
	xdesc = get_rule_desc(xrule)
	rule_key = get_rule_key(xrule)
	if rule_key in pylint_rules_descr:
		update_node_text(xdesc, pylint_rules_descr[rule_key])
	else:
		if rule_key == 'W0199' and 'Did you mean ' not in xdesc.text:
			update_node_text(xdesc, xdesc.text + ' Did you mean \'assert x,y\'?')
	update_node_text(xdesc, get_fixed_text(get_clean_desc_txt(xdesc.text)))
	
	emit = 'This message can\'t be emitted when using Python >= '
	p = xdesc.text.find(emit)
	if p != -1:
		desc_pre = xdesc.text[0:p].strip()
		if len(desc_pre) > 0:
			desc_pre = desc_pre.rstrip('.') + '.'
		desc_end = xdesc.text[p:]
		desc = desc_pre + re.sub(emit + '([0-9\.]+)', '\n' + emit + '\\1\n', desc_end)
		update_node_text(xdesc, desc, True)

def update_rule_status(xrule):
	xdesc = get_rule_desc(xrule)
	rule_key = get_rule_key(xrule)
	rule_version = get_rule_version(xrule)
	if rule_key in pylint_deprecated:
		if rule_version is not None:
			added = 'added in Pylint %s and ' % rule_version
			rule_version = None
		else:
			added = ''
		depr = pylint_deprecated[rule_key]
		text = get_clean_desc_txt(xdesc.text)
		if type(depr) is list:
			if len(depr) == 1:
				text += "\nThis rule is deprecated. It was %sremoved in Pylint %s." % (added, depr[0])
			else:
				text += "\nThis rule is deprecated. It was %sreplaced with {%s} in Pylint %s." % (added, depr[1], depr[0])
		else:
			text += "\nThis rule is deprecated, use {%s} instead." % depr
		update_node_text(xdesc, text, True)
		
		xstatus = xrule.find('status')
		if xstatus is not None:
			xrule.remove(xstatus)
		xstatus = etree.SubElement(xrule, 'status')
		xstatus.text = 'DEPRECATED'
	
	if rule_version is not None:
		text = get_clean_desc_txt(xdesc.text) +  "\nThis rule was added in Pylint %s." % rule_version
		update_node_text(xdesc, text, True)

def pad_desc(text):
	rp = re.compile(r'(<description>)(.*)(</description>)', flags=re.DOTALL)
	mx = rp.search(text)
	if mx is not None:
		desc = mx.group(2).strip().replace("\n", "\n             ")
		text = rp.sub('\\1\n    ' + desc + '\n  \\3', text)
	return text

def pad_rule(text):
	return re.sub(r'^(.*)$', '  \\1', text, flags=re.MULTILINE)

def output_rule(xrule):
	rule_key = get_rule_key(xrule)
	rule_version = get_rule_version(xrule)
	
	update_rule_name(xrule)
	update_rule_priortiy(xrule)
	update_rule_description(xrule)
	update_rule_status(xrule)
	
	rule_str = etree.tostring(xrule, pretty_print=True).strip()
	rule_str = pad_desc(rule_str)
	rule_str = pad_rule(rule_str)
	
	_out(rule_str)

if __name__ == '__main__':
	txt = StringIO(sys.stdin.read());
	parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
	itree = etree.parse(txt, parser)
	
	# get rule nodes
	irules_flat = {}
	iroot = itree.getroot()
	for irule in iroot.iter('rule'):
		irule_key = irule.find('key')
		if irule_key is None: continue
		rule_key = irule_key.text
		irules_flat[rule_key] = irule
	
	# add missing rules
	for rule_key in sorted(pylint_missing_rules):
		if rule_key not in irules_flat:
			prev_rule_key = pylint_missing_rules[rule_key][0]
			if prev_rule_key in irules_flat:
				new_irule = etree.Element('rule')
				new_irule_key = etree.SubElement(new_irule, 'key')
				new_irule_key.text = rule_key
				new_irule_name = etree.SubElement(new_irule, 'name')
				new_irule_name.text = etree.CDATA(pylint_missing_rules[rule_key][1])
				new_irule_ckey = etree.SubElement(new_irule, 'configKey')
				new_irule_ckey.text = rule_key
				new_irule_desc = etree.SubElement(new_irule, 'description')
				new_irule_desc.text = etree.CDATA(pylint_missing_rules[rule_key][2])
				iroot.insert(iroot.index(irules_flat[prev_rule_key]) + 1, new_irule)
				irules_flat[rule_key] = new_irule
	irules_flat = None
	
	# sort rules
	irules = [[], [], [], []]
	for irule in iroot.iter('rule'):
		irule_key = irule.find('key')
		if irule_key is None: continue
		rule_key = irule_key.text
		if rule_key in pylint_rule_order_1:
			irules[0].append(irule)
		elif rule_key in pylint_rule_order_2:
			irules[1].append(irule)
		elif rule_key in pylint_rule_order_3:
			irules[2].append(irule)
		else:
			irules[3].append(irule)
	
	_out('<?xml version="1.0" encoding="UTF-8"?>')
	_out('<rules>')
	for irule in irules[0]: 
		output_rule(irule)
	for irule in irules[1]: 
		output_rule(irule)
	for irule in irules[2]: 
		output_rule(irule)
	for irule in irules[3]: 
		output_rule(irule)
	_out()
	_out('</rules>')
