### Alex's Genetic Programming Algorithm
### ------------------------------------

### For documentation see Genetic Programming I, II & III (Koza et al 199x)

### ===== RELEASE 0.02 ==== 31.12.2001

### Copyright (C) 2001 Alex Wilding
### If you modify this code, either for your own purposes or otherwise,
### PLEASE PLEASE PLEASE PLEASE PLEASE PLEASE let me know at least what
### you have done, or better, send me the source.

### This source is licensed under the GNU General Public License.
### The GPL can be accessed at: http://www.gnu.org/licenses/gpl.html

### This program is free software; you can redistribute it and/or
### modify it under the terms of the GNU General Public License
### as published by the Free Software Foundation; either version 2
### of the License, or any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import math
import random, whrandom
import string
from copy import deepcopy, copy
import sys
import time

####################### RUN PARAMETERS

popcount = 2000
matesubset = 400
genmax = -1
initialdepth = 3



def GetFitness(Ind, verbosefile=None):      ## MODIFY ME FOR DIFFERENT PROBLEMS
  AbsoluteMaxNodes = 35
  parsimony = float(float(max(0,AbsoluteMaxNodes-len(GetIndividualTree(Ind))))/AbsoluteMaxNodes)   # between 0 and 1

  #print parsimony
  # target remains stationary, while mx moves in direction determined by result. If result is positive, move right. If negative, move left.
#  for i in range(100): # run the simulation for 100 cycles.
#    a = ev(Ind.Events[0]);
#    # move a maximum of 10 units.
#    v = v + max(-2,min(2,v))
#    v = v * 0.9;
#    x = x + v;

  # Initialisation
  a = random.random()*100
  x = 10*math.sin(a)
  y = 10*math.cos(a)
  Steps = 20
  for count in range(Steps):
    Ind.Parameters()[0] = x
    Ind.Parameters()[1] = y
#    if verbosefile != None:
#      verbosefile.write(str(x)+","+str(y)+",")
    angle = ev(Ind.Events[0])
    x = x + math.cos(angle)*1
    y = y + math.sin(angle)*1
    if math.sqrt(x*x+y*y) < 0.5:
      break
#  if verbosefile != None:
#    verbosefile.write("\n");  

#  Ind.MyParams[0] = random.random();
#  Ind.MyParams[1] = random.random();
#  angle = ev(Ind.Events[0]);

  result = count
  ideal = 0
  maximum = Steps
  parsimonyweight = 1
  # End fitenss calculation. Do not change.
  fitness =max(maximum-abs(result-ideal),0)
  
  # regulate to non-negative only.
  fitness = float(max(0,fitness));  # fitness is 100-end distance from target.
  return [(100-parsimonyweight)*(fitness/maximum)+parsimony*parsimonyweight,fitness,parsimony]




pass #################################### ** Init:
TNone = -1
TInteger = 0
TBoolean = 1
TFloat = 2
pop = []
newpop = []
ind = 0
pass #################################### ** ABSTRACT NODES
class Node:
  def __init__(self, fIndividual, fParent, fChildren = []):
    #if type(fIndividual) != type(Individual()):
    #  print "NO!" + str(fIndividual)
    self.OutType = TNone
    self.Parent = fParent
    self.AcceptsTypes = []
    self.Children = fChildren
    self.Individual = fIndividual
    self.Name = "Abstract"
    #print "My Children: (should be none)" + str(self.Children)
    #print "My Children: (should be none)" + str(fChildren)
    #print "My Parent: " + str(fParent);
    #print "My Individual: " + str(fIndividual);
    #print "Created"
  #def __str__(self):
  #  return str(ev(self))
  def __eval__(self):
    return "Abstract Base Class"
  def Accepts(self,ftype):
    for q in self.AcceptsTypes:
      if q == ftype:
        return 1
    return 0
  def __tree__(self, indent):
    # printing of node tree
    r =  indent+self.Name+": "+str(self)+"\n"
    for child in self.Children:
      r = r + child.__tree__(indent+"  ")
    return r
  def __random__(self, depth=1):
    pass
  def __text__(self):
    return ""
  def __fix__(self):
    pass
  def __whichchild__(self,aChild):
    for i in range(len(self.Children)):
      if aChild == self.Children[i]:
        return i
  def __route__(self):
    # find the route to this node recursively. If the parent is None, return [].
    # the leftmost entry in the list is the most significant, eg. closest to the root.
    if self.Parent == None:
      return []
    else:
      return self.Parent.__route__() + [self.Parent.__whichchild__(self)]

class LiteralNode(Node):
  def __init__(self, fIndividual, fParent, fChildren = []):
    Node.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Abstract Literal"
  def __eval__(self):
    return "Abstract Literal"
  def __text__(self):    # This is the only type of abstract node that always has the same __text__
    return str(self.val)

class LinkNode(Node):
  def __init__(self, fIndividual, fParent, fChildren = []):
    Node.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Abstract Link"
    self.called = 0
  def __eval__(self):
    # Evaluate all of the children, then pass them to the function self.evaluate.
    #
    # NOTE: This is PRE-ORDER traversal. This means the leaves are always executed
    #       BEFORE THE BRANCHES.    
    ChildEval = []
    for child in self.Children:
      ChildEval = ChildEval + [ev(child)]
    # The answers are now in ChildEval. Pass them to the function.
    return self.evaluate(ChildEval)
  def GetRandomChildren(self,depth = 1): # This is a bit legacy. Should be bundled with __random__
    #global ind
    #ind = ind + 1
    #indd= ('  '*ind)
    #print indd + str(self.called);
    #print indd + str(self.Children);
    for i in range(len(self.Children)):
      #if self.Children[i] != None:
      ##    Either we're mutating, or something's gone horribly, horribly wrong.
      #  print ('  '*ind)+'ARCHGG! '+self.Children[i].Name;

      # Find a type for the new child.
      ChildType = FindMeAChild((depth==0))
      # Create an object of this type
      self.Children[i] = ChildType(self.Individual,self)
      #print indd+str(ChildType)
      #print indd+'Should be none'+str(self.Children[i].Children)
      self.Children[i].__random__(depth-1)
    #ind = ind - 1
    #for child in self.Children:
    #  child.__random__(1)
#    if self.Parent != None:
#      s = 'parent='+self.Parent.Name
#    else:
#      s = 'ROOT'
#    print self.Name + ' - '+ str(len(self.Children))+' d:'+str(depth)+' '+s+'  r: '+str(self.__route__())
#    q = ''
#    for child in self.Children:
#      q = q + child.Name + ', ';
#    print q
#    for child in self.Children:
#      print '  '+child.__text__()
    
  def __fix__(self):
    for child in self.Children:
      child.Parent = self
      child.__fix__()
  def __random__(self, depth = 1):
    self.GetRandomChildren(depth)
    
# These are just as linknode, but with more default children.
# Use these if you're terminally lazy :)
class UnaryNode(LinkNode):           
  def __init__(self, fIndividual, fParent, fChildren = [None]):
    #LinkNode.__init__(self, fIndividual, fParent, fChildren);
    LinkNode.__init__(self, fIndividual, fParent, [None])
    self.Name = "Abstract Unary"
  def evaluate(self, params):
    return params[0]
class BinaryNode(LinkNode):
  def __init__(self, fIndividual, fParent, fChildren = [None, None]):
    #LinkNode.__init__(self, fIndividual, fParent, fChildren);
    LinkNode.__init__(self, fIndividual, fParent, [None, None])

class ThreewayNode(LinkNode):
  def __init__(self, fIndividual, fParent, fChildren = [None, None, None]):
    #LinkNode.__init__(self, fIndividual, fParent, fChildren);
    LinkNode.__init__(self, fIndividual, fParent, [None, None, None])
    
class ComparativeBinaryNode(BinaryNode): # Legacy
  def __init__(self, fIndividual, fParent, fChildren = [None, None]):
    BinaryNode.__init__(self, fIndividual, fParent,fChildren)


pass #################################### ** SPECIFIC NODES
pass ################ (Literals)
class IntegerLiteralNode(LiteralNode):
  def __init__(self, fIndividual, fParent, fChildren = []):
    LiteralNode.__init__(self, fIndividual, fParent, fChildren)
    self.val = 0
    self.Name = "Integer Literal"
  def __eval__(self):
    return self.val
  def __random__(self, depth=1):
    self.val = int(random.gauss(0,10.0)*random.gauss(0,10.0))

class BooleanLiteralNode(LiteralNode):
  def __init__(self, fIndividual, fParent, fChildren = []):
    LiteralNode.__init__(self, fIndividual, fParent, fChildren)
    self.val = 0
    self.Name = "Boolean Literal"
  def __eval__(self):
    return self.val
  def __random__(self, depth=1):
    self.val = random.choice(range(2)); # chooses 0 or 1 randomly.

class FloatLiteralNode(LiteralNode):
  def __init__(self, fIndividual, fParent, fChildren = []):
    LiteralNode.__init__(self, fIndividual, fParent, fChildren)
    self.val = float(0)
    self.Name = "Float Literal"
  def __eval__(self):
    return self.val
  def __random__(self, depth = 1):
    self.val = (random.gauss(0,1.0))  # Gauss distro. Good as any.

class ParameterLiteralNode(LiteralNode):
  def __init__(self, fIndividual, fParent, fChildren = []):
    LiteralNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Parameter Literal"
    self.ParamID = -1
  def __eval__(self):
    if self.ParamID > -1:
      return self.Individual.Parameters()[self.ParamID]
    else:
      return 0
  def __random__(self, depth = 1):
#    try:
      self.ParamID = random.choice(range(len(self.Individual.Parameters()))) # select a random parameter to reference.
#    except:
#      self.ParamID = -1;
  def __text__(self):
    return "P["+str(self.ParamID)+"]"

Literals = [IntegerLiteralNode, BooleanLiteralNode, FloatLiteralNode, ParameterLiteralNode]
pass ################ (Unaries)
class SineUnaryNode(UnaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None]):
    UnaryNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Sine Unary"
#    if isinstance(self.Children[0],Node):
#      if not self.Accepts(self.Children[0].OutType):
#        print "ERROR - Sine Unary Create attempted with wrong type"
        # raise an error or something?
  def evaluate(self,params):
    return math.sin(params[0])
  def __text__(self):
    return "sin("+self.Children[0].__text__()+")"

class CosineUnaryNode(UnaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None]):
    UnaryNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Cosine Unary"
  def evaluate(self, params):
    return math.cos(params[0])
  def __text__(self):
    return "cos("+self.Children[0].__text__()+")"

class AbsUnaryNode(UnaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None]):
    UnaryNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Abs Unary"
  def evaluate(self,params):
    return abs(params[0])
  def __text__(self):
    return "abs("+self.Children[0].__text__()+")"

class NegateUnaryNode(UnaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None]):
    UnaryNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Negate Unary"
  def evalaute(self,params):
    return -(params[0])
  def __text__(self):
    return "(-("+self.Children[0].__text__()+"))"

class SquareRootUnaryNode(UnaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None]):
    UnaryNode.__init__(self, fIndividual, fParent,fChildren)
    self.Name = "Square Root Unary"
  def evaluate(self,params):
    return math.sqrt(abs(params[0]))
  def __text__(self):
    return "sqrt("+self.Children[0].__text__()+")"

class SquareUnaryNode(UnaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None]):
    UnaryNode.__init__(self, fIndividual, fParent,fChildren)
    self.Name = "Square Unary"
  def evaluate(self, params):
    return (params[0])**2
  def __text__(self):
    return "sqr("+self.Children[0].__text__()+")"

class PassThroughUnaryNode(UnaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None]):
    UnaryNode.__init__(self, fIndividual, fParent,fChildren)
    self.Name = "PassThrough Unary"
  def evaluate(self,params):
    return params[0]
  def __text__(self):
    return self.Children[0].__text__()

Unaries = [SineUnaryNode, CosineUnaryNode, AbsUnaryNode, NegateUnaryNode, SquareRootUnaryNode, SquareUnaryNode]
pass ################ (Binaries)
class AddBinaryNode(BinaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None, None]):
    BinaryNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Add Binary"
  def evaluate(self, params):
    return params[0] + params[1]
  def __text__(self):
    return "("+self.Children[0].__text__()+"+"+self.Children[1].__text__()+")"

class ArcTan2BinaryNode(BinaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None, None]):
    BinaryNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "ArcTan2 Binary"
  def evaluate(self, params):
    return math.atan2(params[0],params[1])
  def __text__(self):
    return "arctan2("+self.Children[0].__text__()+","+self.Children[1].__text__()+")"

class SubtractBinaryNode(BinaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None, None]):
    BinaryNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Subtract Binary"
  def evaluate(self,params):
    return params[0] - params[1]
  def __text__(self):
    return "("+self.Children[0].__text__()+"-"+self.Children[1].__text__()+")"

class MultiplyBinaryNode(BinaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None, None]):
    BinaryNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Multiply Binary"
  def evaluate(self,params):
    return params[0] * params[1]
  def __text__(self):
    return "("+self.Children[0].__text__()+"*"+self.Children[1].__text__()+")"

class DivideBinaryNode(BinaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None, None]):
    BinaryNode.__init__(self, fIndividual, fParent, fChildren)
    self.Name = "Divide Binary"
  def evaluate(self, params):
    try:
      return params[0]/params[1]
    except:
      return 0
  def __text__(self):
    return "("+self.Children[0].__text__()+"/"+self.Children[1].__text__()+")"

class LessEqualBinaryNode(ComparativeBinaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None, None]):
    ComparativeBinaryNode.__init__(self, fIndividual, fParent,fChildren)
    self.Name = "Lesser/Equal Binary Node"
  def evaluate(self, params):
    return (params[0] <= params[1])
  def __text__(self):
    return "isLessEqual("+self.Children[0].__text__()+", "+self.Children[1].__text__()+")"

class GreaterEqualBinaryNode(ComparativeBinaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None, None]):
    ComparativeBinaryNode.__init__(self, fIndividual, fParent,fChildren)
    self.Name = "Greater/Equal Binary Node"
  def evaluate(self, params):
    return (params[0] <= params[1])
  def __text__(self):
    return "isGreaterEqual("+self.Children[0].__text__()+", "+self.Children[1].__text__()+")"

class PowerBinaryNode(BinaryNode):
  def __init__(self, fIndividual, fParent, fChildren = [None,None]):
    BinaryNode.__init__(self, fIndividual, fParent,fChildren)
    self.Name = "Raise To Power Binary Node"
  def evaluate(self, params):
    try:
      return math.pow(abs(params[0]),params[1])
    except:
      return 0
  def __text__(self):
    return "pow("+self.Children[0].__text__()+","+self.Children[1].__text__()+")"

Binaries = [ArcTan2BinaryNode, AddBinaryNode, SubtractBinaryNode, MultiplyBinaryNode, DivideBinaryNode, PowerBinaryNode,LessEqualBinaryNode,GreaterEqualBinaryNode]
pass ################ (Threeways)
class IsNearThreewayNode(ThreewayNode): # Target, Try, Radius
  def __init__(self, fIndividual, fParent, fChildren = [None,None, None]):
    ThreewayNode.__init__(self, fIndividual, fParent,fChildren)
    self.Name = "Is Near Threeway Node"
  def evaluate(self, params):
    return (abs(params[0]-params[1]) <= abs(params[2]))

class ConditionalThreewayNode(ThreewayNode):
  def __init__(self, fIndividual, fParent, fChildren = [None,None, None]):
    ThreewayNode.__init__(self, fIndividual, fParent,fChildren)
    self.OutType = TBoolean
    self.AcceptsTypes = [TFloat, TBoolean, TInteger]
    self.Name = "Comparative Threeway Node"
  def __eval__(self): # This is a special case. A VERY SPECIAL CASE. The code might not be executed for one branch.
    if (ev(self.Children[0])) > 0: # come to think of it, all structural absurdities will be like this. Oh well :)
      return ev(self.Children[1])
    else:
      return ev(self.Children[2])
  def __text__(self):
    return "cond("+self.Children[0].__text__()+", "+self.Children[1].__text__()+", "+self.Children[2].__text__()+")"

Threeways = [ConditionalThreewayNode] #IsNearThreewayNode, 
pass #################################### ** Helper Functions
Nodes = Literals + Unaries + Binaries + Threeways
NodeTypes = {}
# Make a dictionary of every result type.
#for noddy in Nodes:
#  NodeTypes.update({ noddy :noddy(None, None).OutType})

def ev(N):
  return N.__eval__()

def randomize(N, depth = 1): # randomizes an instance rather than creating an instance
  N.__random__(depth)

def FindMeAChild(Terminal): # terminal says we must not return a linking node. Returns a *type*
  # Don't do type checking anymore.
  
#  ShortList = [];
#  TypeList = list(Types)
  if Terminal:
    LongList = Literals
  else:
    LongList = Nodes
#  for n in LongList:
#    if TypeList.count(NodeTypes[n]) > 0:
#      ShortList.append(n);
  return whrandom.choice(LongList)

# Generate complete list of node types available.
pass #################################### ** GA Classes

stepsize = (popcount / 70)
if stepsize == 0:
  stepsize = 1

class Individual:
  def __init__(self):
    self.Events = [PassThroughUnaryNode(self,None)]
    self.Fitness = []
    self.MyParams = []
  def __random__(self,depth = 11):
    for R in self.Events:
      randomize(R,depth)
  def Parameters(self):
    return self.MyParams

def GetIndividualTree(Ind):
  res = []
  for e in Ind.Events:
    res = res + GetTree(e)
  return res

def GetTree(Root): # return all nodes under a tree as a list. (for randomly picking a node)
  res = Root.Children
  for C in Root.Children:
    res = res + GetTree(C)
  return res

def OldMate(ParentA, ParentB): # sexually mate the two parents, and return a child individual (1/5)
  # Mate two parents to produce an offspring.
  # Deep copies ParentA to Child, then finds an appropriate match of a subtree between Child and ParentB,
  # and moves the subtree from ParentB to Child. If no match can be found, None is returned as the individuals
  # are incompatible.
  
  # CHANGE ME:
  # Alter this routine so that the pieces swapped are in roughly the same place in the tree.
  # A node is chosen randomly, and the route through the tree (which Children are selected)
  # is calculated. This route is applied to the other tree, so a node of equivalent position
  # is swapped, instead of something that will clearly destroy genetic information.
  # Q: What will odd positioning lead to - ie. if a node can't even nearly reach a position?
  Child = Individual()
  Child.Events = deepcopy(ParentA.Events)
  Rind = random.randint(0,len(Child.Events)-1)
  
  SourceNode = random.choice(GetTree(ParentB.Events[Rind]))
  TargetNode = random.choice(GetTree(Child.Events[Rind]))
  #print "Source: "+SourceNode.__text__()
  #print "Target: "+TargetNode.__text__()
  TargetParent = TargetNode.Parent
  if TargetParent != None:
  #  print "Switching"
    TargetParentChildIndex = WhichChild(TargetNode, TargetParent)
  TargetNode = deepcopy(SourceNode)
  if TargetParent != None:
    TargetNode.Parent = TargetParent;  # stitch it on
    TargetParent.Children[TargetParentChildIndex] = TargetNode
  
  # During mating, the backreferences to the base individuals and the immediate parents get
  # a little scrambled. Brute force fix this. Not very efficient, but whattaya gonna do?
  for e in Child.Events:
    for n in GetTree(e):
      n.Individual = Child
    e.__fix__()
  return Child

def MateIndividuals(ParentA, ParentB): # Depricate me! Replace with the all-seeing Program node
  Child = Individual()
  Child.Events = [Mate([ParentA.Events[0],ParentB.Events[0]], Child)]
  Child.MyParams = [0,0]
  for n in GetTree(Child.Events[0]):
    n.Individual = Child
  Child.Events[0].__fix__()
  return Child

def Mate(Parents, aIndividual): # sexually mate any number of nodes to make new nodes. (5/5)
  # Amalgamating Crossover. True to real life. Breed (5/5).
  # Parents are parent NODES not individuals.
  # Which one will it be?
  Parent = random.choice(Parents)
  NewNode = copy(Parent)
  # Now go through the children and mate them too. If there are no children, don't.
  for i in range(len(NewNode.Children)): # only count up to the new node's children. If there are none, sobeit.
    PossibleChildren = []
    for aParent in Parents:
      if i < len(aParent.Children):
        # if this parent has an applicable child
        PossibleChildren = PossibleChildren + [copy(aParent.Children[i])]
    for child in PossibleChildren: #Fix the OO linkage.
      child.Parent = NewNode
      child.Individual = aIndividual
    NewNode.Children[i] = Mate(PossibleChildren, aIndividual)
  return NewNode

def Mutate(Ind): # mutate a subtree of this individual
  # select a subtree and randomize it. This could easily kill the organism, but is needed to stop the gene pool
  # getting stagnant.
  MuteNode = random.choice(GetTree(random.choice(Ind.Events)))
  randomize(MuteNode,initialdepth)

# All objects are in place. GAtastic!

def ChooseRandom(Population): # choose a random individual based on fitness
  # NOTE TO ME: This is a shit and inefficient way of doing things. It'd be
  # *much* better to have multiple sorted slicepos values, and only calculate
  # the total and iterate once. I'll do this sometime.
  
  # Each member of Population has a non-negative fitness. Find the total.
  # Get a random number 0..total. Walk through the population and stop
  # when the accumulated fitness > the random number.
  # operate on a small subset of nodes. Multiplicity given by matesubset
  # This speeds things up, and it happens in the wild (proximity of couples)
  c = []
  for i in range(matesubset):
    c = c + [random.randint(0,len(pop)-1)]
  total = 0
  for i in c:
    total = total + pop[i].Fitness[0]
  # now total is the total fitness
  # find where in the distribution to drop the pencil
  slicepos = random.random()*total
  tf = 0
  index = 0
  #print "Slicepos = "+str(slicepos)
  while tf < slicepos:
    tf = tf + pop[c[index]].Fitness[0]
    index = index + 1
  # it really buggers if you don't do this. It's a cheap hack.
  index = index - 1
  #print "Chosen "+str(index)+" for parent - fitness" + str(pop[index].Fitness);
  return pop[c[index]]


def pdot(n): # print a little dot to indicate we've done something. Progress indicator
  if n % stepsize == 0:
    sys.stdout.write(".")

def RandomizeIndividual(I, depth):
  I.MyParams = RandomParams()
  I.__random__(depth)
#  for e in I.Events:
#    randomize(e,depth)

def NewPopulation(depth): # randomly initialise a new population up to popcount.
  global pop#, GlobalParameters
  while len(pop) < popcount:
    pdot(len(pop))
    I = Individual()
    RandomizeIndividual(I,depth)
    pop = pop + [I]

def MateAll(): # perform mating on the entire population, kill the parents and replace them with Children
  global pop, newpop
  newpop = []
  #print "Mating:"
  while len(newpop) < popcount: # produce new population by sexual crossover.
 #   try:
      newpop = newpop + [MateIndividuals(ChooseRandom(pop),ChooseRandom(pop))]
      pdot(len(newpop))
 #   except:
      #doesn't matter - just try again!
 #     pass
  #print "Done Mating"
  pop = newpop
  newpop = []
  print("")
  # now we have a new population in wpop.

def GetAllFitness(): #
  # Get the fitness for the whole population and store it in each individuals Fitness property.
  # Individual.Fitness[0] stores the actual fitness. [1] is usually a sample and [2] parsimony (0,1).
  # Where 1 is trivially parsimonious.
  j = 0
  for p in pop:
    try:
      j = j + 1
      pdot(j)
      totfit = 0
      for i in range(10):
        p.MyParams = RandomParams()  # randomize parameters for each test
        p.Fitness = GetFitness(p)
        totfit = totfit + p.Fitness[0]
      p.Fitness[0] = totfit / 10.0
    except: # Stop it from breeding if it excepts. Cruel :)
      print("Error in evaluation")
      p.Fitness = [0,0,0]

# create the population
#GlobalParameters = [0];

def RandomParams():
  # Replace me
  return [0,0]


def ClearFile(filename): # make a blank file and erase any file that's already there.
  fitlog = open(filename,"w")
  fitlog.close()

def WriteToFile(filename, line):
  # Meant for fail-safe, not efficiency. Every time a line is written, it opens and closes the file
  fitlog = open(filename,"a")
  fitlog.write(line)
  fitlog.close()

ClearFile("fitness.csv")
ClearFile("samplelog.csv")
ClearFile("Programs.txt")

gen = 0
print("Generating initial population")
NewPopulation(initialdepth)
while (gen < genmax) or (genmax == -1): # Da Mane Lupe
#while 0:
  # make the global parameters
  #GlobalParameters = [random.random()*3];
  #print GlobalParameters
  print("\nMutating:")
  j = 0
  for p in pop: # mutate a few and randomize the old parameters
    p.MyParams = RandomParams()
    j= j+1
    pdot(j)
    try:
      if random.random() < 0.05: # but not too many
        Mutate(p)
    except:
      pass # who cares?!
  # get the fitness ready for reproduction 
  print("\nFinding Fitness:")
  GetAllFitness()
  qmax = pop[0]
  qmin = pop[0]
  s = 0
  ens = 0
  tot = 0
  print("\nBucketing:")
  bucketcount = 20
  buckets = []
  for i in range(bucketcount+2): buckets.append(0)
  for p in pop:
    buckets[int(bucketcount*(p.Fitness[0]+1)/100.0)] = buckets[int(bucketcount*(p.Fitness[0]+1)/100.0)]+1
  s = ""
  for q in buckets:
    s = s + str(q)+","
  s = s + "\n"
  WriteToFile("fitness.csv",s)
  s = 0
  print("\nGetting Best of Generation:")
  for p in pop: # Get the Best Of Generation
    #p.RootNode.__tree__("  ")
    s = s + 1
    try:
      tot = tot + p.Fitness[0]
      if p.Fitness[0] < qmin.Fitness[0]:
        qmin = p
      if p.Fitness[0] > qmax.Fitness[0]:
        qmax = p
        ens = s
    except:
      print("¶ Error on "+str(s))
      print("p.Fitness = "+ str(p.Fitness))
      print("---------end error report")
  s = "\nNode "+str(ens)+":"+str(qmax.Fitness)
  print("\n")

  besttree = qmax.Events[0].__text__()+"\n"
  print(besttree)
  #print qmax.Events[0].__tree__("  ");

  WriteToFile("Programs.txt",s+"\n"+besttree)

  #---Uncomment to save a sample log to file. Legacy.
  #runlog = open("samplelog.csv","a")
  #GetFitness(qmax,runlog);
  #runlog.close();
  
  print(s)
  # do the reproduction
  print("\nMating for generation "+str(gen)+":")
  MateAll()
  gen = gen + 1

for i in range(1):
  Dummy = Individual()
  Dummy.MyParams = [0,0]
  Dummy2 = Individual()
  Dummy2.MyParams = [0,0]

  RandomizeIndividual(Dummy,4)
  RandomizeIndividual(Dummy2,4)
  #print 'END'+str(i)+'::: '+Dummy.Events[0].__text__()
  
#  Q1 = PassThroughUnaryNode(Dummy, None)
#  Q1.__random__(3)
#  Q2 = PassThroughUnaryNode(Dummy2, None)
#  Q2.__random__(3)
  #print 'Q1: '+Q1.__text__()
  #print "Q2: "+Q2.__text__()
  M = MateIndividuals(Dummy,Dummy2)
  M.MyParams = [0,0]
  print('M:  '+M.Events[0].__text__())
  print(ev(M.Events[0]))
  #print Q.__text__()