# Lola - Dibujar AST + graphviz

import pydotplus as pgv
import ast_lola as ast
import operator

def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        '*' : operator.mul,
        '/' : operator.truediv,
        '%' : operator.mod,
        '^' : operator.xor,
        }[op]

def eval_binary_expr(op1, operator, op2):
    op1,op2 = int(op1), int(op2)
    return get_operator_fn(operator)(op1, op2)
	
class DotCode(ast.NodeVisitor):
	'''
	Clase Node Visitor que crea secuencia de instrucciones Dot
	'''
	
	def __init__(self):
		super(DotCode, self).__init__()
		
		# Secuencia para los nombres de nodos
		self.id = 0
		
		# Stack para retornar nodos procesados
		self.stack = []
		
		# Inicializacion del grafo para Dot
		self.dot = pgv.Dot('AST', graph_type='digraph')  
		
		self.dot.set_node_defaults(shape='box', color='lightgray', style='filled')
		self.dot.set_edge_defaults(arrowhead='none')
		
		#control de chequeo de variables
		self.DeclarandoVariables=None
		self.VisitandoModulo=None
		
		self.typePortsIn=[]
		self.typePortsInOut=[]
		self.typePortsOut=[]
		self.typePortsVar=[]
		self.typeConst=[]
		
		
		self.moduleTypes=[]
		self.modulePortsIn=[]
		self.modulePortsInOut=[]
		self.modulePortsOut=[]
		self.modulePortsVar=[]
		self.moduleConst=[]
		
		self.PortsSize=[]
		self.indexing=[]
		
		#etiquetas de control
		self.StartOperation=False
		self.DeclarandoConstante=False
		self.ValueOperation=0
		self.opSimbolExpresion=None
		self.TipoFormal=False
		self.PortsIn=False
		self.PortsInOut=False
		self.PortsOut=False
		self.PortsVar=False
		self.usingConst=None
		self.dataType=None
		self.StartAssing=True
		self.selectorValue=None
		self.evaluateID=None
		self.evaluateVAR=None
		self.varpos=0
		self.ForValues=[]
		self.diccionarios=[]
		
	def __repr__(self):
		return self.dot.to_string()
	
	def new_node(self, node, label=None, shape='box', color="lightgray"):
		'''
		Crea una variable temporal como nombre del nodo
		'''
		if label is None:
			label = node.__class__.__name__#le entrega al label, es decir nombre el label
		if (node is not None):
			
			if(node.tipo is not None):
				label+=" | "+str(node.tipo)
				#print("label", label)
				#print("tipo nodo", node.tipo)
		
		self.id += 1
		
		return pgv.Node('n{}'.format(self.id), label=label, shape=shape, color=color)

	def visit_Lola(self, node):
		target = self.new_node(node, shape='house')
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		print("\n\nDiccionario\n")
		for dic in self.diccionarios:
			for enum, dicc in enumerate(dic):
				if(enum==0):
					print("MODULO:", dicc)
				if(enum==1):
					print("Types")
					for item in dicc:
						for enumType, itemType in enumerate(item):
							if(enumType==0):
								print("Type:",item[0])
							if(enumType==1):
								print("Type-Puertos IN:")
								for itemitemType in itemType:
									print(itemitemType)
							if(enumType==2):
								print("Type-Puertos INOUT:")
								for itemitemType in itemType:
									print(itemitemType)
							if(enumType==3):
								print("Type-Puertos OUT:")
								for itemitemType in itemType:
									print(itemitemType)
							if(enumType==4):
								print("Type-CONST's:")
								for itemitemType in itemType:
									print(itemitemType)
				if(enum==2):
					print("Puertos IN:")
					for item in dicc:
						print(item)
				if(enum==3):
					print("Puertos INOUT:")
					for item in dicc:
						print(item)
				if(enum==4):
					print("Puertos OUT:")
					for item in dicc:
						print(item)
				if(enum==5):
					print("Puertos VAR:")
					for item in dicc:
						print(item)
				if(enum==6):
					print("CONST's:")
					for item in dicc:
						print(item)
	def visit_Modulo(self, node):
		node.tipo="LOLA-MODULE"
		target = self.new_node(node, None, 'circle', 'white')
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
				if(field=="ID0"):
					if(len(self.diccionarios)>0):
						if(self.diccionarios[len(self.diccionarios)-1][0]==value):
							print("error ya existe modulo", value)
				if(field=="ID1"):
					self.diccionarios.append([value])
					#print(self.diccionarios)
					self.diccionarios[len(self.diccionarios)-1].append(self.moduleTypes)
					self.diccionarios[len(self.diccionarios)-1].append(self.modulePortsIn)
					self.diccionarios[len(self.diccionarios)-1].append(self.modulePortsInOut)
					self.diccionarios[len(self.diccionarios)-1].append(self.modulePortsOut)
					self.diccionarios[len(self.diccionarios)-1].append(self.modulePortsVar)
					self.diccionarios[len(self.diccionarios)-1].append(self.moduleConst)
		
		
		self.typePortsIn=[]
		self.typePortsInOut=[]
		self.typePortsOut=[]
		self.typeConst=[]
		self.typePortsVar=[]
		
		self.moduleTypes=[]
		self.modulePortsIn=[]
		self.modulePortsInOut=[]
		self.modulePortsOut=[]
		self.modulePortsVar=[]
		self.moduleConst=[]
		
		self.PortsSize=[]
		self.TipoDato=None
		self.evaluateID=None
		
		
		
		self.stack.append(target)
	
	def visit_DeclaracionTipoPuntoComa(self, node):
		node.tipo="MODULE-Types"
		target = self.new_node(node, None, 'triangle', 'beige')
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		
		
	def visit_DeclaracionTipo(self, node):
		node.tipo="TYPE"
		target = self.new_node(node)
		self.dot.add_node(target)
		self.typePortsIn=[]
		self.typePortsInOut=[]
		self.typePortsOut=[]
		self.typePortsVar=[]
		self.typeConst=[]
		self.VisitandoModulo=False
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				if(field=="ID0"):
					self.moduleTypes.append([value, None, None, None, None, None])
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.VisitandoModulo=True
		self.moduleTypes[len(self.moduleTypes)-1][1]=self.typePortsIn
		self.moduleTypes[len(self.moduleTypes)-1][2]=self.typePortsInOut
		self.moduleTypes[len(self.moduleTypes)-1][3]=self.typePortsOut
		self.moduleTypes[len(self.moduleTypes)-1][4]=self.typePortsVar
		self.moduleTypes[len(self.moduleTypes)-1][5]=self.typeConst
		
		self.typePortsIn=[]
		self.typePortsInOut=[]
		self.typePortsOut=[]
		self.typePortsVar=[]
		self.typeConst=[]
		
		self.stack.append(target)
		
	def visit_DeclaracionConstanteCONST(self, node):
		if(self.VisitandoModulo):
			node.tipo="MODULE-CONST"
		else:
			node.tipo="TYPE-CONST"
		target = self.new_node(node, None, 'triangle', 'yellow')
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		
	def visit_DeclaracionConstante(self, node):
		if(self.VisitandoModulo):
			node.tipo="MODULE-CONST"
		else:
			node.tipo="TYPE-CONST"
		target = self.new_node(node, shape='octagon', color='yellow')
		self.dot.add_node(target)
		self.DeclarandoConstante=True
		self.DeclarandoVariables=True
		self.StartOperation=False
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			
			if isinstance(value, ast.AST):
				if(field=="expresion" and not self.VisitandoModulo):
					self.typeConst[len(self.typeConst)-1][1]=self.visit(value)
					
				elif(field=="expresion" and self.VisitandoModulo):
					self.moduleConst[len(self.moduleConst)-1][1]=self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				if(field=="ID" and not self.VisitandoModulo):
					self.typeConst.append([value, None])
				elif(field=="ID" and self.VisitandoModulo):
					self.moduleConst.append([value, None])
					
				
				targetHijo = self.new_node(None, value+" | "+node.tipo, 'hexagon', color='yellow')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.StartOperation=False
		self.ValueOperation=0
		self.DeclarandoConstante=False
		self.stack.append(target)
	
	def visit_TipoFormalIN(self, node):
		node.tipo="TYPE-PortsIN"
		target = self.new_node(node, None, 'triangle', 'lightgreen')
		self.dot.add_node(target)
		self.PortsIn=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsIn=False
		self.stack.append(target)
	
	def visit_TipoFormalINOUT(self, node):
		node.tipo="TYPE-PortsINOUT"
		target = self.new_node(node, None, 'triangle', 'orange')
		self.dot.add_node(target)
		self.PortsInOut=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsInOut=False
		self.stack.append(target)
	
	
	def visit_DeclaracionVariableIN(self, node):
		node.tipo="MODULE-PortsIN"
		target = self.new_node(node, None, 'triangle', 'lightgreen')
		self.dot.add_node(target)
		self.PortsIn=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsIn=False
		self.stack.append(target)
	
	def visit_DeclaracionVariableINOUT(self, node):
		node.tipo="MODULE-PortsINOUT"
		target = self.new_node(node, None, 'triangle', 'orange')
		self.dot.add_node(target)
		self.PortsIn=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsIn=False
		self.stack.append(target)
	
	def visit_DeclaracionVariableOUT(self, node):
		if(self.VisitandoModulo):
			node.tipo="MODULE-PortsOUT"
		else:
			node.tipo="TYPE-PortsOUT"
		target = self.new_node(node, None, 'triangle', 'pink')
		self.dot.add_node(target)
		self.PortsOut=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsOut=False
		self.stack.append(target)
		
	def visit_DeclaracionVariableVAR(self, node):
		node.tipo="MODULE-PortsVAR"
		target = self.new_node(node, None, 'triangle', 'violet')
		self.dot.add_node(target)
		self.PortsVar=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.PortsVar=False
		self.stack.append(target)
	
	def visit_TipoFormallistaIdR(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.PortsSize=[]
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		
	def visit_TipoFormalINOUT(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.PortsSize=[]
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
	
	
	def visit_DeclaracionVariableRecursivoR(self, node):
		if(self.PortsIn):
			target = self.new_node(node, shape='octagon', color='lightgreen')
		else:
			target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.PortsSize=[]
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		
		
		
	def visit_Tipo(self, node):
		target = self.new_node(node)
		if(self.VisitandoModulo):
			
			if(self.PortsIn):
				node.tipo="MODULE-PortsIN"
				target = self.new_node(node, shape='octagon', color='lightgreen')
			if(self.PortsInOut):
				node.tipo="MODULE-PortsINOUT"
				target = self.new_node(node, shape='octagon', color='orange')
			if(self.PortsOut):
				node.tipo="MODULE-PortsOUT"
				target = self.new_node(node, shape='octagon', color='pink')
			if(self.PortsVar):
				node.tipo="MODULE-PortsVar"
				target = self.new_node(node, shape='octagon', color='violet')
		else:
			if(self.PortsIn):
				node.tipo="TYPE-PortsIN"
				target = self.new_node(node, shape='octagon', color='lightgreen')
			if(self.PortsInOut):
				node.tipo="TYPE-PortsINOUT"
				target = self.new_node(node, shape='octagon', color='orange')
			if(self.PortsOut):
				node.tipo="TYPE-PortsOUT"
				target = self.new_node(node, shape='octagon', color='pink')
			if(self.PortsVar):
				node.tipo="TYPE-PortsVar"
				target = self.new_node(node, shape='octagon', color='violet')
		
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(field=="tipoExpresiones" and value is None):
				self.PortsSize.append(1)
		self.stack.append(target)
		
	
	
	def visit_TipoExpresionesR(self, node):
		target = self.new_node(node)
		if(self.VisitandoModulo):
			
			if(self.PortsIn):
				node.tipo="MODULE-PortsIN"
				target = self.new_node(node, shape='octagon', color='lightgreen')
			if(self.PortsInOut):
				node.tipo="MODULE-PortsINOUT"
				target = self.new_node(node, shape='octagon', color='orange')
			if(self.PortsOut):
				node.tipo="MODULE-PortsOUT"
				target = self.new_node(node, shape='octagon', color='pink')
			if(self.PortsVar):
				node.tipo="MODULE-PortsVar"
				target = self.new_node(node, shape='octagon', color='violet')
		else:
			if(self.PortsIn):
				node.tipo="TYPE-PortsIN"
				target = self.new_node(node, shape='octagon', color='lightgreen')
			if(self.PortsInOut):
				node.tipo="TYPE-PortsINOUT"
				target = self.new_node(node, shape='octagon', color='orange')
			if(self.PortsOut):
				node.tipo="TYPE-PortsOUT"
				target = self.new_node(node, shape='octagon', color='pink')
			if(self.PortsVar):
				node.tipo="TYPE-PortsVar"
				target = self.new_node(node, shape='octagon', color='violet')
		
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						resize=self.visit(item)
						#print("value resize", resize)
						self.PortsSize.append(resize)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
	
	def visit_TipoFormal(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.TipoFormal=True
		setup=False
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				if(not self.VisitandoModulo):
					if(self.PortsIn):
						for Ports in self.typePortsIn:
							if(Ports[1] is None):
								Ports[1]=[self.PortsSize[0]]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports[1].append(resize)
								Ports.append("BIT")
								
							
					if(self.PortsInOut):
						for Ports in self.typePortsInOut:
							if(Ports[1] is None):
								Ports[1]=[self.PortsSize[0]]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports[1].append(resize)
								Ports.append("BIT")
								
					if(self.PortsOut):
						for Ports in self.typePortsOut:
							if(Ports[1] is None):
								Ports[1]=[self.PortsSize[0]]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports[1].append(resize)
								Ports.append("BIT")
					if(self.PortsVar):
						for Ports in self.typePortsVar:
							if(Ports[1] is None):
								Ports[1]=[self.PortsSize[0]]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports[1].append(resize)
								Ports.append("BIT")
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
				setup=True
		if(not setup):
			
			if(not self.VisitandoModulo):
				if(self.PortsIn):
					for Ports in self.typePortsIn:
						if(Ports[1] is None):
							Ports[1]=[1]
							Ports.append("BIT")
							#print(Ports)
						
				if(self.PortsInOut):
					for Ports in self.typePortsInOut:
						if(Ports[1] is None):
							Ports[1]=[1]
							Ports.append("BIT")
				if(self.PortsOut):
					for Ports in self.typePortsOut:
						if(Ports[1] is None):
							Ports[1]=[1]
							Ports.append("BIT")
				if(self.PortsVar):
					for Ports in self.typePortsVar:
						if(Ports[1] is None):
							Ports[1]=[1]
							Ports.append("BIT")
		self.TipoFormal=False
		self.stack.append(target)
		
	def visit_TipoFormalBus(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		#self.TipoFormal=True
		setup=False
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				if(not self.VisitandoModulo):
					if(self.PortsIn):
						for Ports in self.typePortsIn:
							if(Ports[1] is None):
								Ports[1]=[self.PortsSize[0]]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports[1].append(resize)
								Ports.append("NOTVALUE")
								
							
					if(self.PortsInOut):
						for Ports in self.typePortsInOut:
							if(Ports[1] is None):
								Ports[1]=[self.PortsSize[0]]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports[1].append(resize)
								Ports.append("NOTVALUE")
								
					if(self.PortsOut):
						for Ports in self.typePortsOut:
							if(Ports[1] is None):
								Ports[1]=[self.PortsSize[0]]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports[1].append(resize)
								Ports.append("NOTVALUE")
					if(self.PortsVar):
						for Ports in self.typePortsVar:
							if(Ports[1] is None):
								Ports[1]=[self.PortsSize[0]]
								if(len(self.PortsSize)>1):
									for resize in self.PortsSize:
										Ports[1].append(resize)
								Ports.append("NOTVALUE")
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
				setup=True
			elif(value is not None):
				if(not setup):
			
					if(not self.VisitandoModulo):
						if(self.PortsIn):
							for Ports in self.typePortsIn:
								if(Ports[1] is None):
									Ports[1]=[1]
									Ports.append("NOTVALUE")
									#print(Ports)
								
						if(self.PortsInOut):
							for Ports in self.typePortsInOut:
								if(Ports[1] is None):
									Ports[1]=[1]
									Ports.append("NOTVALUE")
						if(self.PortsOut):
							for Ports in self.typePortsOut:
								if(Ports[1] is None):
									Ports[1]=[1]
									Ports.append("NOTVALUE")
						if(self.PortsVar):
							for Ports in self.typePortsVar:
								if(Ports[1] is None):
									Ports[1]=[1]
									Ports.append("NOTVALUE")
				if(self.PortsIn):
					for Ports in self.typePortsIn:
						if(Ports[len(Ports)-1]=="NOTVALUE"):
							Ports[len(Ports)-1]==value
						
				if(self.PortsInOut):
					for Ports in self.typePortsInOut:
						if(Ports[len(Ports)-1]=="NOTVALUE"):
							Ports[len(Ports)-1]==value
				if(self.PortsOut):
					for Ports in self.typePortsOut:
						if(Ports[len(Ports)-1]=="NOTVALUE"):
							Ports[len(Ports)-1]==value
				if(self.PortsVar):
					for Ports in self.typePortsVar:
						if(Ports[len(Ports)-1]=="NOTVALUE"):
							Ports[len(Ports)-1]==value
				else:
					if(self.PortsIn):
						for Ports in self.typePortsIn:
							if(Ports[len(Ports)-1]=="NOTVALUE"):
								Ports[len(Ports)-1]==value
							
					if(self.PortsInOut):
						for Ports in self.typePortsInOut:
							if(Ports[len(Ports)-1]=="NOTVALUE"):
								Ports[len(Ports)-1]==value
					if(self.PortsOut):
						for Ports in self.typePortsOut:
							if(Ports[len(Ports)-1]=="NOTVALUE"):
								Ports[len(Ports)-1]==value
					if(self.PortsVar):
						for Ports in self.typePortsVar:
							if(Ports[len(Ports)-1]=="NOTVALUE"):
								Ports[len(Ports)-1]==value
		
		
		
		#self.TipoFormal=False
		self.stack.append(target)
	
	def visit_TipoSimpleBasico(self, node):
		target = self.new_node(node)
		if(self.VisitandoModulo):
			
			if(self.PortsIn):
				node.tipo="MODULE-PortsIN"
				target = self.new_node(node, shape='octagon', color='lightgreen')
			if(self.PortsInOut):
				node.tipo="MODULE-PortsINOUT"
				target = self.new_node(node, shape='octagon', color='orange')
			if(self.PortsOut):
				node.tipo="MODULE-PortsOUT"
				target = self.new_node(node, shape='octagon', color='pink')
			if(self.PortsVar):
				node.tipo="MODULE-PortsVar"
				target = self.new_node(node, shape='octagon', color='violet')
		else:
			if(self.PortsIn):
				node.tipo="TYPE-PortsIN"
				target = self.new_node(node, shape='octagon', color='lightgreen')
			if(self.PortsInOut):
				node.tipo="TYPE-PortsINOUT"
				target = self.new_node(node, shape='octagon', color='orange')
			if(self.PortsOut):
				node.tipo="TYPE-PortsOUT"
				target = self.new_node(node, shape='octagon', color='pink')
			if(self.PortsVar):
				node.tipo="TYPE-PortsVAR"
				target = self.new_node(node, shape='octagon', color='violet')
		
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if(value is not None):#ramas...
				targetHijo = self.new_node(None, label=value)
				if(not self.VisitandoModulo):
					if(self.PortsIn):
						for Ports in self.typePortsIn:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
								#print(Ports)
						targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsIN", shape='hexagon', color='lightgreen')
							
					if(self.PortsInOut):
						for Ports in self.typePortsInOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
						targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsINOUT", shape='hexagon', color='orange')
					if(self.PortsOut):
						for Ports in self.typePortsOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
						targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsOUT", shape='hexagon', color='pink')
					if(self.PortsVar):
						for Ports in self.typePortsVar:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
						targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsVar", shape='hexagon', color='violet')
				elif(self.VisitandoModulo):
					
					if(self.PortsIn):
						for Ports in self.modulePortsIn:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
						targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsIN", shape='hexagon', color='lightgreen')
							
					if(self.PortsInOut):
						for Ports in self.modulePortsInOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
						targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsINOUT", shape='hexagon', color='orange')
					if(self.PortsOut):
						for Ports in self.modulePortsOut:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
						targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsOUT", shape='hexagon', color='pink')
					if(self.PortsVar):
						for Ports in self.modulePortsVar:
							if(Ports[1] is None):
								Ports[1]=self.PortsSize
								for resize in self.PortsSize:
									Ports[1]=self.PortsSize
								Ports.append(value)
						targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsVar", shape='hexagon', color='violet')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
	
	def visit_TipoSimpleID(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if(value is not None):#ramas...
				if(self.PortsVar):
					existValue=False
					for Ports in self.modulePortsVar:
						if(Ports[1] is None):
							
							#print("types de modulo valor:",self.moduleTypes)
							
							Ports[1]=self.PortsSize
							for resize in self.PortsSize:
								Ports[1]=self.PortsSize
								
							for findPort in self.moduleTypes:
								if(findPort[0]==value):
									Ports.append(findPort)
									existValue=True
									targetHijo = self.new_node(None, str(value)+" | "+"MODULE-TYPES", shape='hexagon', color='violet')
									break
							if(not existValue):
								targetHijo = self.new_node(None, value, 'diamond')
								print("el type {} no fue declarado".format(value))
								
							#print("valor ports var:",Ports)
							
				else:
					print("solo se pueden declar de tipos de Types declarados en VAR")
					targetHijo = self.new_node(None, value, 'diamond')
				
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
	
	def visit_ExpresionCorcheteOR(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.ValueOperation=None
						self.StartOperation=False
						resize=self.visit(item)
						print("valor resize", resize)
						if(resize is None):
							self.PortsSize.append(-1)
						else:
							self.PortsSize(resize)
						print("valor portssize ", self.PortsSize)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
	
	def visit_ExpresionOpcional(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			
			if isinstance(value, ast.AST):
				resize=self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		return resize
	
	def visit_Expresion(self, node):
		if(self.DeclarandoConstante):
			if(self.VisitandoModulo):
				node.tipo="MODULE-CONST"
				
				#print("aqui")
			else:
			
				node.tipo="TYPE-CONST"
			target = self.new_node(node, shape='octagon', color='yellow')
		else:
			target = self.new_node(node)
		self.dot.add_node(target)
		
				
			
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						termvalue=self.visit(item)
						if(not self.StartOperation):
							self.ValueOperation=termvalue
							self.StartOperation=True
						elif((self.opSimbolExpresion=="+" or self.opSimbolExpresion=="-" or self.opSimbolExpresion=="/" or self.opSimbolExpresion=="MOD") and self.DeclarandoConstante and isinstance(self.ValueOperation, int) and isinstance(termvalue, int)):
							self.ValueOperation=eval_binary_expr(self.ValueOperation, self.opSimbolExpresion, termvalue)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						self.opSimbolExpresion=item
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
		return self.ValueOperation
		
		
	def visit_Termino(self, node):
		if(self.DeclarandoConstante):
			if(self.VisitandoModulo):
				node.tipo="MODULE-CONST"
				
				#print("aqui")
			else:
			
				node.tipo="TYPE-CONST"
			target = self.new_node(node, shape='octagon', color='yellow')
		else:
			target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						termvalue=self.visit(item)
						if(not self.StartOperation):
							self.ValueOperation=termvalue
							self.StartOperation=True
						elif((self.opSimbolExpresion=="+" or self.opSimbolExpresion=="-" or self.opSimbolExpresion=="/" or self.opSimbolExpresion=="MOD") and self.DeclarandoConstante and isinstance(self.ValueOperation, int) and isinstance(termvalue, int)):
							self.ValueOperation= eval_binary_expr(self.ValueOperation, self.opSimbolExpresion, termvalue)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
						self.stack.append(target)
						
					elif(item is not None):#caso de ramas
						
						self.opSimbolExpresion=item
						targetHijo = self.new_node(None, item)
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))	
		self.stack.append(target)
		return self.ValueOperation
		
		
	def visit_FactorValor(self, node):
		if(self.DeclarandoConstante):
			if(self.VisitandoModulo):
				node.tipo="MODULE-CONST"
				
				#print("aqui")
			else:
			
				node.tipo="TYPE-CONST"
			target = self.new_node(node, shape='octagon', color='yellow')
		else:
			target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if(value is not None):
				targetHijo = self.new_node(None, value)
				if(self.DeclarandoConstante):
					targetHijo = self.new_node(None, str(value)+" | "+node.tipo+"-INTEGER",shape='hexagon', color='yellow')
				elif(isinstance(value, int)):
					if(self.VisitandoModulo):
						targetHijo = self.new_node(None, str(value)+" | "+"MODULE-INTEGER",shape='hexagon', color='yellow')
					else:
						targetHijo = self.new_node(None, str(value)+" | "+"TYPE-INTEGER",shape='hexagon', color='yellow')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
				
		self.stack.append(target)
		return value
		
	
	def visit_FactorSelector(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if(field=="ID"):
				self.selectorValue=value
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				
				existValue=False
				if(not self.VisitandoModulo):
					self.usingConst=None
					for valuei in self.typeConst:
						if(valuei[0]==value):
							self.usingConst=valuei[1]
							existValue=True
							targetHijo = self.new_node(None, label=value+" | "+"TYPE-CONST", shape='hexagon', color='yellow')
					
					if(self.StartAssing):
						for Ports in self.typePortsIn:
							if(Ports[0]==value):
								self.selectorValue=value
								existValue=True
								targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsIN", shape='hexagon', color='lightgreen')
								if(Ports[len(Ports)-1]!=self.dataType):
									
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
									
						for Ports in self.typePortsInOut:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsINOUT", shape='hexagon', color='orange')
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						for Ports in self.typePortsOut:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsOUT", shape='hexagon', color='pink')
								print("Error el puerto de salida debe ser resultado de una asignación, valor", value)
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						for Ports in self.typePortsVar:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsVAR", shape='hexagon', color='violet')
								#print("Error el puerto de salida debe ser resultado de una asignación, valor", value)
								#if(Ports[len(Ports)-1]!=self.dataType):
									#print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						
							
					if(not existValue):
						print("{} no ha sido declarado".format(value))
						targetHijo = self.new_node(None, value, 'diamond')
				elif(self.VisitandoModulo):#verificar esto
					self.usingConst=None
					for valuei in self.moduleConst:
						if(valuei[0]==value):
							self.usingConst=valuei[1]
							existValue=True
							targetHijo = self.new_node(None, label=value+" | "+"MODULE-CONST", shape='hexagon', color='yellow')
					for valuei in self.ForValues:
						if(valuei[0]==value):
							existValue=True
							
							targetHijo = self.new_node(None, label=value+" | "+"MODULE-FOR-VALUE", shape='hexagon', color='yellow')
					if(self.StartAssing):
						for Ports in self.modulePortsIn:
							if(Ports[0]==value):
								self.selectorValue=value
								existValue=True
								targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsIN", shape='hexagon', color='lightgreen')
								if(self.evaluateVAR is not None):
									if(len(self.evaluateVAR[1])<self.varpos):
										self.dataType=self.evaluateVAR[1][self.varpos][len(self.evaluateVAR[1][self.varpos])-1]
										self.varpos+=1
								else:
									self.dataType="error"
									print("Mal uso de asignación de unidad, no es coherente la cantidad de puertos del TYPE", self.self.evaluateVAR[0])
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
									
						for Ports in self.modulePortsInOut:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsINOUT", shape='hexagon', color='orange')
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						for Ports in self.modulePortsOut:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsOUT", shape='hexagon', color='pink')
								print("Error el puerto de salida debe ser resultado de una asignación, valor", value)
								if(Ports[len(Ports)-1]!=self.dataType):
									print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						
						for Ports in self.modulePortsVar:
							if(Ports[0]==value):
								selectorValue=value
								existValue=True
								targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsVAR", shape='hexagon', color='violet')
								#if(Ports[len(Ports)-1]!=self.dataType):
									#print("Error en uso de variables, los tipos de dato no coinciden con el valor", value)
						
						
					if(not existValue):
						print("{} no ha sido declarado".format(value))
						targetHijo = self.new_node(None, value, 'diamond')
				#print(targetHijo)
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
				
				
		
		self.stack.append(target)
		return self.usingConst
		
	
	def visit_ListaId(self, node):
		target = self.new_node(node)
		if(self.VisitandoModulo):
			
			if(self.PortsIn):
				node.tipo="MODULE-PortsIN"
				target = self.new_node(node, shape='octagon', color='lightgreen')
			if(self.PortsInOut):
				node.tipo="MODULE-PortsINOUT"
				target = self.new_node(node, shape='octagon', color='orange')
			if(self.PortsOut):
				node.tipo="MODULE-PortsOUT"
				target = self.new_node(node, shape='octagon', color='pink')
			if(self.PortsVar):
				node.tipo="MODULE-PortsVar"
				target = self.new_node(node, shape='octagon', color='violet')
		else:
			if(self.PortsIn):
				node.tipo="TYPE-PortsIN"
				target = self.new_node(node, shape='octagon', color='lightgreen')
			if(self.PortsInOut):
				node.tipo="TYPE-PortsINOUT"
				target = self.new_node(node, shape='octagon', color='orange')
			if(self.PortsOut):
				node.tipo="TYPE-PortsOUT"
				target = self.new_node(node, shape='octagon', color='pink')
			if(self.PortsVar):
				node.tipo="TYPE-PortsVar"
				target = self.new_node(node, shape='octagon', color='violet')
		
		
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item)
						if(not self.VisitandoModulo):
							#print("agrege typesIDs como ", item)
							existValue=False
							pos=None
							#print(item)
							for enum, Ports in enumerate(self.typePortsIn):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.typePortsIn[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de TYPE".format(item))
									
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.typePortsInOut):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.typePortsInOut[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de TYPE".format(item))
								
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.typePortsOut):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.typePortsVar):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.typePortsOut[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de TYPE".format(item))
							if(self.PortsIn):
								self.typePortsIn.append([item, None])
								targetHijo = self.new_node(None, item+" | TYPE-PortsIN", shape='hexagon', color='lightgreen')
							if(self.PortsInOut):
								self.typePortsInOut.append([item, None])
								targetHijo = self.new_node(None, item+" | TYPE-PortsINOUT", shape='hexagon', color='orange')
							if(self.PortsOut):
								self.typePortsOut.append([item, None])
								targetHijo = self.new_node(None, item+" | TYPE-PortsOUT", shape='hexagon', color='pink')
							if(self.PortsVar):
								self.typePortsVar.append([item, None])
								targetHijo = self.new_node(None, item+" | TYPE-PortsVAR", shape='hexagon', color='violet')
							
							
							#print(self.typesIDs)
						elif(self.VisitandoModulo):
							#print("agrege moduleIDs como ", item)
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.modulePortsIn):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.modulePortsIn[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de MODULE".format(item))
									
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.modulePortsInOut):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							if(existValue):
								del self.modulePortsInOut[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de MODULE".format(item))
								
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.modulePortsOut):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break
							existValue=False
							pos=None
							for enum, Ports in enumerate(self.modulePortsVar):
								if(Ports[0]==item):
									existValue=True
									pos=enum
									break		
									
							if(existValue):
								del self.modulePortsOut[pos];
								print("peligro redeclarando valor {} que estaba en puertos de entrada de TYPE".format(item))
							if(self.PortsIn):
								self.modulePortsIn.append([item, None])
								targetHijo = self.new_node(None, item+" | MODULE-PortsIN", shape='hexagon', color='lightgreen')
							if(self.PortsOut):
								self.modulePortsOut.append([item, None])
								targetHijo = self.new_node(None, item+" | MODULE-PortsOUT", shape='hexagon', color='pink')
							if(self.PortsInOut):
								self.modulePortsInOut.append([item, None])
								targetHijo = self.new_node(None, item+" | MODULE-PortsINOUT", shape='hexagon', color='orange')
							if(self.PortsVar):
								self.modulePortsVar.append([item, None])
								targetHijo = self.new_node(None, item+" | MODULE-PortsVAR", shape='hexagon', color='violet')
							#print(self.moduleIDs)
							#self.moduleIDs.append(item)
						
						
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value)
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
	
	def visit_AsignacionUnidad(self, node):
		if(self.VisitandoModulo):
			node.tipo="MODULE-Sentencias"
		else:
			node.tipo="TYPE-Sentencias"
			print("No es posible aplicar asignación de unidad en TYPE")
		
		target = self.new_node(node, shape='parallelogram', color='lightblue')
		self.dot.add_node(target)
		self.varpos=0
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				if(field=="ID"):
					
					self.selectorValue=value
					existValue=False
					for Ports in self.modulePortsVar:
						if(Ports[0]==value):
							self.evaluateVAR=Ports
							existValue=True
							targetHijo = self.new_node(None, value+" | "+"MODULE-PortsVAR", shape='hexagon', color='violet')
							break
					if(not existValue):
						print("el valor {} no existe como VAR o no está declarado")
				
				#self.dataType
				
				
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.evaluateVAR=None
		self.stack.append(target)
	
	
	def visit_selectorR(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		index=0
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						if (self.VisitandoModulo):
							for ID in self.modulePortsIn:
								if(self.selectorValue==ID[0]):
									if(not (len(ID[1])-1>index or len(ID[1])==0)):
										print("Error de indexado con la variable", ID)
									index+=1
							for ID in self.modulePortsInOut:
								if(self.selectorValue==ID[0]):
									if(not (len(ID[1])-1>index or len(ID[1])==0)):
										print("Error de indexado con la variable", ID)
									index+=1
							for ID in self.modulePortsOut:
								if(self.selectorValue==ID[0]):
									if(not (len(ID[1])-1>index or len(ID[1])==0)):
										print("Error de indexado con la variable", ID)
									index+=1
							for ID in self.modulePortsVar:
								if(self.selectorValue==ID[0]):
									if(not (len(ID[1])-1>index or len(ID[1])==0)):
										print("Error de indexado con la variable", ID)
									index+=1
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
	
	def visit_SelectorRR(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				tempvalue=self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				if isinstance(value, int):
					if(self.VisitandoModulo):
						targetHijo = self.new_node(None, str(value)+" | "+"MODULE-INTEGER", shape='hexagon', color='yellow')
					else:
						targetHijo = self.new_node(None, str(value)+" | "+"TYPE-INTEGER", shape='hexagon', color='yellow')
				for valuei in self.ForValues:
					if(valuei[0]==value):
						if(self.VisitandoModulo):
							targetHijo = self.new_node(None, str(value)+" | "+"MODULE-FOR-VALUE", shape='hexagon', color='yellow')
						else:
							targetHijo = self.new_node(None, str(value)+" | "+"TYPE-FOR-VALUE", shape='hexagon', color='yellow')
						
				if(self.StartAssing):
					for valuei in self.modulePortsVar:
						#print("selectorr",value)
						#print("valuei",valuei[0], self.selectorValue)
						if(valuei[0]==self.selectorValue):
							#print("valuei", valuei[2][1])
							for item in valuei[2][1]:#entrada
								#print("algo",item[0], value)
								if(item[0]==value):
									#print("otro",value)
									targetHijo = self.new_node(None, value+" | "+"MODULE-TYPE-PortsIN", shape='hexagon', color='lightgreen')
									if(item[len(item)-1]!=self.dataType):
										print("no coinciden los datos del VAR {} puerto {}".format(self.selectorValue, value))
							for item in valuei[2][2]:#entradasalida
								#print("algo",item[0], value)
								if(item[0]==value):
									#print("otro",value)
									targetHijo = self.new_node(None, value+" | "+"MODULE-TYPE-PortsINOUT", shape='hexagon', color='orange')
									if(item[len(item)-1]!=self.dataType):
										print("no coinciden los datos del VAR {} puerto {}".format(self.selectorValue, value))
						for item in valuei[2][3]:#entradasalida
								#print("algo",item[0], value)
								if(item[0]==value):
									#print("otro",value)
									targetHijo = self.new_node(None, value+" | "+"MODULE-TYPE-PortsOUT", shape='hexagon', color='pink')
									if(item[len(item)-1]!=self.dataType):
										print("no coinciden los datos del VAR {} puerto {}".format(self.selectorValue, value))
				
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
				tempvalue=value
		self.stack.append(target)
		return tempvalue
		
		
		
		
	def visit_SentenciaSecuenciaBEGIN(self, node):
		if(self.VisitandoModulo):
			node.tipo="MODULE-Sentencias"
		else:
			node.tipo="TYPE-Sentencias"
		target = self.new_node(node, None, 'triangle', 'lightblue')
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
		self.stack.append(target)
		
	def visit_Asignacion(self, node):
		if(self.VisitandoModulo):
			node.tipo="MODULE-Sentencias"
		else:
			node.tipo="TYPE-Sentencias"
		target = self.new_node(node, shape='parallelogram', color='lightblue')
		self.dot.add_node(target)
		self.StartAssing=True
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				
				if(field=="ID"):
					if(not self.VisitandoModulo):
						existValue=False
						if(self.StartAssing):
							for valuei in self.typeConst:
								if(valuei[0]==value):
									print("No se puede asignar modos de conexión a una constante, valor", value)
									existValue=True
									targetHijo = self.new_node(None, label=value+" | "+"TYPE-CONST", shape='hexagon', color='yellow')
							for Ports in self.typePortsIn:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									print("error, un puerto de entrada no puede ser resultado, valor", value)
									targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsIN", shape='hexagon', color='lightgreen')
							for Ports in self.typePortsInOut:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									self.dataType=Ports[len(Ports)-1]
									targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsINOUT", shape='hexagon', color='orange')
							for Ports in self.typePortsOut:
								if(Ports[0]==value):
									if(Ports[0]==value):
										#self.selectorValue=value
										existValue=True
										self.dataType=Ports[len(Ports)-1]
										targetHijo = self.new_node(None, label=value+" | "+"TYPE-PortsOUT", shape='hexagon', color='pink')
										#print("port:",Ports)
										#print("colocando tipo ", self.dataType)
								
						if(not existValue):
							print("{} no ha sido declarado".format(value))
							targetHijo = self.new_node(None, value, 'diamond')
					elif(self.VisitandoModulo):#verificar esto
						existValue=False
						#print("aqui")
						for valuei in self.moduleConst:
							if(valuei[0]==value):
								print("No se puede dar modos de conexión a una constante, valor", value)
								targetHijo = self.new_node(None, label=value+" | "+"MODULE-CONST", shape='hexagon', color='yellow')
						if(self.StartAssing):
							for Ports in self.modulePortsIn:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									print("error, un puerto de entrada no puede ser resultado, valor", value)
									targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsIN", shape='hexagon', color='lightgreen')
										
							for Ports in self.modulePortsInOut:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									self.dataType=Ports[len(Ports)-1]
									targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsINOUT", shape='hexagon', color='orange')
							for Ports in self.modulePortsOut:
								if(Ports[0]==value):
									#self.selectorValue=value
									existValue=True
									self.dataType=Ports[len(Ports)-1]
									targetHijo = self.new_node(None, label=value+" | "+"MODULE-PortsOUT", shape='hexagon', color='pink')
									
									
						if(not existValue):
							print("{} no ha sido declarado".format(value))
							targetHijo = self.new_node(None, value, 'diamond')
					
					

				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)	
	
	def visit_SentenciaPara(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				if(field=="ID"):
					for valuei in self.ForValues:
						if(valeui[0]==value):
							print("peligro, redeclarando valor iterador de for", value)
							self.ForValues.remove(valuei)
					self.ForValues.append((value, None))
				
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.ForValues=[]
		self.stack.append(target)

	
	def generic_visit(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		self.stack.append(target)
		
		

