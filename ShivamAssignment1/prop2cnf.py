# File made available through the generosity of Prof. Ioerger, TAMU.

import sys,re

# could add <-, <->, xor

def tokenize(s):
  words = re.findall('\->|[\|\&\^\-\(\)]|[A-Za-z0-9_]*',s)
  return filter(lambda x: x!='',words)

def parse(tokens): return parse1(tokens,0,len(tokens))[0]

def parse1(toks,i,n):
  nodes = []
  while i<n and toks[i]!=')':
    if toks[i]=='(':
      subtree,j = parse1(toks,i+1,n)
      nodes.append(subtree)
      i = j+1
    else: nodes.append(toks[i]); i += 1
  nodes = shift_reduce(nodes)
  return nodes,i

def prec(tok):
  if tok in ['and','&']: return 3
  if tok in ['or','|']: return 2
  if tok in ['implies','->']: return 1
  return 0

opers = "and or implies & | ->".split()

neg = 'not -'.split()

def shift_reduce(nodes):
  i,n = 1,len(nodes)
  stack = [nodes[0]] # initialize
  while True:
    if len(stack)>=1 and stack[-1] in neg: stack.append(nodes[i]); i += 1
    elif len(stack)>=2 and stack[-2] in neg: a,b = stack[:-2],stack[-2:]; stack = a; stack.append(b)
    elif len(stack)>=3 and stack[-2] in opers:
      if i==n or (nodes[i] in opers and prec(stack[-2])>=prec(nodes[i])):
        stack = stack[:-3]+[[stack[-2],stack[-3],stack[-1]]] # prefix not., oper first
      else: stack.append(nodes[i]); i += 1
    elif i==n:
      if len(stack)!=1: error('syntax error: %s' % nodes)
      else: return stack[0]
    else: stack.append(nodes[i]); i += 1

def convert2cnf(tree):
  verbose = False
  if verbose==True: print 'convert:',tree
  tree = implication_elimination(tree)
  if verbose==True: print 'Im_elim:',tree
  tree = push_negations_inward(tree)
  if verbose==True: print 'pushneg:',tree
  tree = distribute(tree)
  if verbose==True: print 'distrib:',tree
  tree = clausify(tree)
  if verbose==True: print 'clauses:',tree
  return tree

# assume in CNF form, represented as binary tree; collect disjunctions

def clausify(tree):
  if isinstance(tree,list)==False: return [[tree]]
  if tree[0] in ['and','&']: return clausify(tree[1])+clausify(tree[2])
  elif tree[0] in ['or','|']: return [collect_literals(tree)]
  else: return [[tree]]

def collect_literals(tree):
  if isinstance(tree,list)==True and tree[0] in ['or','|']: 
    return collect_literals(tree[1])+collect_literals(tree[2])
  else: return [tree]

def implication_elimination(tree):
  if isinstance(tree,list)==False: return tree
  subexpressions = map(implication_elimination,tree)
  if tree[0] in ['implies','->']:
    return ['or',['not',subexpressions[1]],subexpressions[2]]
  else: return subexpressions

# DeMorgan's laws, double-negation elimination, assume no implications

def push_negations_inward(tree):
  if isinstance(tree,list)==False: return tree
  if tree[0] in ['not','-']:
    if tree[1][0] in ['not','-']: 
      return push_negations_inward(tree[1][1])
    if tree[1][0] in ['or','|']: 
      return push_negations_inward(['and',['not',tree[1][1]],['not',tree[1][2]]])
    if tree[1][0] in ['and','&']: 
      return push_negations_inward(['or',['not',tree[1][1]],['not',tree[1][2]]])
    else: return map(push_negations_inward,tree)
  else: return map(push_negations_inward,tree)

# (a & b) | X -> (a | X) & (b | X)
# X | (a & b) -> distibute of reverse

def distribute(tree):
  if isinstance(tree,list)==False: return tree
  if tree[0] in ['or','|']:
    if tree[1][0] in ['and','&']: 
      return distribute(['and',['or',tree[1][1],tree[2]],['or',tree[1][2],tree[2]]])
    elif tree[2][0] in ['and','&']: 
      return distribute(['or',tree[2],tree[1]])
    else: return map(distribute,tree)
  else: return map(distribute,tree)

def error(msg):
  print msg
  sys.exit(0)

if __name__=="__main__":
  clauses = []
  for line in open(sys.argv[1]):
    line = line.rstrip()
    # upper case?
    if len(line)==0 or line[0]=='#': continue
    tokens = tokenize(line)
    tree = parse(tokens)
    cnf = convert2cnf(tree)
    print 'c original :',line
    print 'c parsetree:',tree
    print 'c clauses  :',cnf
    print 'c'
    clauses += cnf

  symbols = {}
  numeric_clauses = []
  cnt = 1
  for clause in clauses:
    numeric = []
    for literal in clause: 
      if isinstance(literal,list)==True: is_negation = True
      else: is_negation = False
      if is_negation==True: proposition = literal[1]
      else: proposition = literal
      if proposition not in symbols: symbols[proposition] = cnt; cnt += 1
      id = symbols[proposition]
      if is_negation==True: numeric.append(-id)
      else: numeric.append(id)
    numeric_clauses.append(numeric)

  print 'c'
  symbols2 = [(symbols[x],x) for x in symbols.keys()]
  symbols2.sort()
  for (id,sym) in symbols2:
    print 'c %s = %s' % (id,sym)
  print 'c'

  print 'p cnf %d %d' % (len(symbols),len(clauses))

  for clause in numeric_clauses:
    for x in clause: print x,
    print 0
  print '0'
