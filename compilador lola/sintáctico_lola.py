from sly import Parser
from léxico_lola import CalcLexer
from ast_lola import *
from loladot import *
from lolacode import *
class CalcParser(Parser):
	debugfile='parser.out'#control de depuración
	tokens = CalcLexer.tokens
	start = 'lola'

	def __init__(self):
		self.errorStatus=False
		
	'''
	lola : lola module
	| module
	;
	'''
	@_('lola modulo')
	def lola(self, p):
		if(self.errorStatus or p.lola is None):
			return
		else:
			p.lola.append(p.modulo)
			return p.lola
	
	@_('modulo')
	def lola(self, p):
		if(self.errorStatus):
			return
		else:
			return Lola([p.modulo])
			
	'''
	tipoSimple : tipoBasico
		|	ID "(" listaExpresiones ")"
		|	ID
		;
	'''
	@_('tipoBasico') 
	def tipoSimple(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoSimpleBasico(p.tipoBasico)#valor constante
	
	@_('ID "(" listaExpresiones ")"')
	def tipoSimple(self, p):
		if(self.errorStatus):
			return
		else:
			node=TipoSimpleIDListaExpresion(p.ID, p.listaExpresiones)
			node.lineno=p.lineno
			return node
	
	@_('ID')
	def tipoSimple(self, p):
		if(self.errorStatus):
			return
		else:
			node=TipoSimpleID(p.ID)
			node.lineno=p.lineno
			return node
		
	'''
	tipoBasico : 'BIT'
		| 'TS'
		| 'OC'
		;
	'''
	@_('BIT', 
	'TS', 
	'OC')
	def tipoBasico(self, p):
		if(self.errorStatus):
			return
		else:
			return p[0]#valor constante
		
	'''
	listaExpresiones : listaExpresiones "," expresion
		| expresion
		;
	'''
	@_('listaExpresiones "," expresion')
	def listaExpresiones(self, p):
		if(self.errorStatus or p.listaExpresiones is None):
			return
		else:
			p.listaExpresiones.append(p.expresion)
			return p.listaExpresiones

	@_('expresion')
	def listaExpresiones(self, p):
		if(self.errorStatus):
			return
		else:
			return ListaExpresiones([p.expresion])
		
	'''
	tipo : tipoExpresiones tipoSimple
	;
	'''
	@_('tipoExpresiones tipoSimple')
	def tipo(self, p):
		if(self.errorStatus):
			return
		else:
			return Tipo(p.tipoExpresiones, p.tipoSimple)
	
	'''
	tipoExpresiones : tipoExpresionesR
	|	empty
	;
	'''
	@_('tipoExpresionesR')
	def tipoExpresiones(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoExpresiones(p.tipoExpresionesR)
	
	@_('empty')
	def tipoExpresiones(self, p):
		return None
	
	'''
	tipoExpresionesR : tipoExpresionesR "[" expresion "]"
	|	"[" expresion "]"
	;
	'''
	@_('tipoExpresionesR "[" expresion "]"')
	def tipoExpresionesR(self, p):
		if(self.errorStatus or p.tipoExpresionesR is None):
			return
		else:
			p.tipoExpresionesR.append(p.expresion)
			return p.tipoExpresionesR
		
	@_('"[" expresion "]"')
	def tipoExpresionesR(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoExpresionesR([p.expresion])
	
	'''
	declaracionConstante : ID DOSPUNTOSIGUAL expresion ";"'
	;
	'''
	@_('ID DOSPUNTOSIGUAL expresion ";"')
	def declaracionConstante(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionConstante(p.ID, p.expresion)
	
	'''
	declaracionVariable : listaId ":" tipo ";"
	;
	'''
	@_('listaId ":" tipo ";"')
	def declaracionVariable(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariable(p.listaId, p.tipo)
	
	'''
	listaId : listaId "," ID
		|	ID
		;
	'''
	@_('listaId "," ID')
	def listaId(self, p):
		if(self.errorStatus or p.listaId is None):
			return
		else:
			p.listaId.append(p.ID)
			return p.listaId
	
	@_('ID')
	def listaId(self, p):
		if(self.errorStatus):
			return
		else:
			return ListaId([p.ID])
	
	'''
	selector : selectorR
	|	empty
	;
	'''
	
	@_('selectorR')
	def selector(self, p):
		if(self.errorStatus):
			return
		else:
			return Selector(p.selectorR)
	
	@_('empty')
	def selector(self, p):
		return None
	
	'''
	selectoR : selectorR selectorRR
	|	selectorRR
	;
	'''
	@_('selectorR selectorRR')
	def selectorR(self, p):
		if(self.errorStatus or p.selectorR is None):
			return
		else:
			p.selectorR.append(p.selectorRR)
			return p.selectorR
		
	@_('selectorRR')
	def selectorR(self, p):
		if(self.errorStatus):
			return
		else:
			return SelectorR([p.selectorRR])
		
	'''
	selectorRR : "." ID
	|	"." INTEGER
	|	"[" expresion "]"
	;
	'''
	@_('"." ID')
	def selectorRR(self, p):
		if(self.errorStatus):
			return
		else:
			return SelectorRR(p[1], None, None)
	
	@_('"." INTEGER')
	def selectorRR(self, p):
		if(self.errorStatus):
			return
		else:
			return SelectorRR(None, p[1], None)
			
	@_('"[" expresion "]"')
	def selectorRR(self, p):
		if(self.errorStatus):
			return
		else:
			return SelectorRR(None, None, p[1])
		
	'''
	factor : ID selector
	|	valorLogico
	|	INTEGER
	|	"~" factor
	|	'FLECHAARRIBA factor'
	|	"(" expresion ")"
	|	"MUX" "(" expresion ":" expresion "," expresion ")"
	|	"MUX" "(" expresion "," expresion ":" expresion "," expresion "," expresion "," expresion)
	|	"REG" "(" expresion ")"
	|	"REG" "(" expresion "," expresion ")"
	|	"LATCH" "(" expresion "," expresion ")"
	|	"SR" "(" expresion "," expresion ")"
	;
	'''
	#'"↑" factor', genera error de enconding
	@_('ID selector')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorSelector(p.ID, p.selector)
		
	
	@_('LOGICVALUE')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorValor(p.LOGICVALUE)
		
	@_('INTEGER')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorValor(p.INTEGER)
		
	@_('FLECHAARRIBA factor')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:	
			return FactorSimbolo(p.FLECHAARRIBA, p.factor)
		
	@_('"~" factor')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorSimbolo(p[0], p.factor)
		
	@_('"(" expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion((p[0], p[2]), [p.expresion])
		
	@_('MUX "(" expresion ":" expresion "," expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.MUX, [p.expresion0, p.expresion1, p.expresion2])
		
	@_('MUX "(" expresion "," expresion ":" expresion "," expresion "," expresion "," expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.MUX, [p.expresion0, p.expresion1, p.expresion2, p.expresion3, p.expresion4, p.expresion5])
	
	@_('REG "(" expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.REG, [p.expresion])
	
	@_('REG "(" expresion "," expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.MUX, [p.expresion0, p.expresion1])
		
	@_('LATCH "(" expresion "," expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.LATCH, [p.expresion0, p.expresion1])
		
	@_('SR "(" expresion , expresion ")"')
	def factor(self, p):
		if(self.errorStatus):
			return
		else:
			return FactorDeclaracion(p.SR, p.expresion0, p.expresion1)
	
	'''
	termino : termino simbolosProd factor
	|	factor
	;
	'''	
	@_('termino "*" factor', 'termino "/" factor', 'termino DIV factor', 'termino MOD factor')
	def termino(self, p):
		if(self.errorStatus or p.termino is None):
			return
		else:
			p[0].append(p[1], p[2])
			return p[0]
	
	@_('factor')
	def termino(self, p):
		if(self.errorStatus):
			return
		else:
			return Termino([None],[p.factor])
	

		
	'''
	expresion : expresion "+" termino
	|	expresion "-" termino
	|	termino
	;
	'''
	@_('expresion "+" termino',
	'expresion "-" termino')
	def expresion(self, p):
		if(self.errorStatus or p[0] is None):
			return
		else:
			p[0].append(p[1], p[2])
			return p[0]
		
	@_('termino')
	def expresion(self, p):
		if(self.errorStatus):
			return
		else:
			return Expresion([None], [p.termino])
		
	'''
	asignacion : ID selector DOSPUNTOSIGUAL expresion
	|	ID selector DOSPUNTOSIGUAL condicion "|" expresion
	;
	'''
	@_('ID selector DOSPUNTOSIGUAL expresion')
	def asignacion(self, p):
		if(self.errorStatus):
			return
		else:
			return Asignacion(p.ID, p.selector, p.expresion)
	
	@_('ID selector DOSPUNTOSIGUAL condicion "|" expresion')
	def asignacion(self, p):
		if(self.errorStatus):
			return
		else:
			return AsignacionCondicion(p.ID, p.selector, p.condicion, p.expresion)
	
	'''
	condicion : expresion
	;
	'''
	@_('expresion')
	def condicion(self, p):
		if(self.errorStatus):
			return
		else:
			return Condicion(p.expresion)
	
	'''
	relacion : expresion "=" expresion
	|	expresion "#" expresion
	|	expresion "<" expresion
	|	expresion MENORIGUAL expresion
	|	expresion ">" expresion
	|	expresion MAYORIGUAL expresion
	;
	'''
	@_('expresion "=" expresion',
	'expresion "#" expresion',
	'expresion "<" expresion',
	'expresion MENORIGUAL expresion',
	'expresion ">" expresion',
	'expresion MAYORIGUAL expresion')
	def relacion(self, p):
		if(self.errorStatus):
			return
		else:
			return Relacion(p[0], p[1], p[2])
		
	'''
	sentenciaSi : "IF" relacion "THEN" sentenciaSecuencia sentenciaSiSino sentenciaSiEntonces "END"
	;
	'''
	@_('IF relacion THEN sentenciaSecuencia sentenciaSiSino sentenciaSiEntonces END')
	def sentenciaSi(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSi(p.relacion, p.sentenciaSecuencia, p.sentenciaSiSino, p.sentenciaSiEntonces)
		
	'''
	sentenciaSiSino : sentenciaSiSinoR
	|	empty
	;
	'''
	@_('sentenciaSiSinoR')
	def sentenciaSiSino(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSiSino(p.sentenciaSiSinoR)
		
	@_('empty')
	def sentenciaSiSino(self, p):
		return None
	
	'''
	sentenciaSiSinoR : sentenciaSiSinoR "ELSIF" relacion "THEN" sentenciaSecuencia
	|	"ELSIF" relacion "THEN" sentenciaSecuencia
	;
	'''
	
	@_('sentenciaSiSinoR ELSIF relacion THEN sentenciaSecuencia')
	def sentenciaSiSinoR(self, p):
		if(self.errorStatus or p.sentenciaSiSinoR):
			return
		else:
			p.sentenciaSiSinoR.append(p.relacion, p.sentenciaSecuencia)
			return p.sentenciaSiSinoR
	
	@_('ELSIF relacion THEN sentenciaSecuencia')
	def sentenciaSiSinoR(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSiSinoR([p.relacion], [p.sentenciaSecuencia])
	
	'''
	sentenciaSiEntonces : "ELSE" sentenciaSecuencia
	|	empty
	;
	'''
	@_('ELSE sentenciaSecuencia')
	def sentenciaSiEntonces(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSiEntonces(p.sentenciaSecuencia)
	
	@_('empty')
	def sentenciaSiEntonces(self, p):
		return None
	
	'''
	sentenciaPara : "FOR" ID ":=" expresion DOBLEPUNTO expresion "DO" sentenciaSecuencia "END"
	;
	'''
	@_('FOR ID DOSPUNTOSIGUAL expresion DOBLEPUNTO expresion DO sentenciaSecuencia END')
	def sentenciaPara(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaPara(p.ID, p.expresion0, p.expresion1, p.sentenciaSecuencia)
		
	'''
	sentencia : asignacion
	|	asignacionUnidad
	|	sentenciaSi
	|	sentenciaPara
	|	empty
	;
	'''
	@_('asignacion', 
	'asignacionUnidad', 
	'sentenciaSi', 
	'sentenciaPara')
	def sentencia(self, p):
		if(self.errorStatus):
			return
		else:
			return Sentencia(p[0])
	
	@_('empty')
	def sentencia(self, p):
		return None
	
	'''
	sentenciaSecuencia : sentenciaSecuencia ";" sentencia
	|	sentencia
	;
	'''
	@_('sentenciaSecuencia ";" sentencia')
	def sentenciaSecuencia(self, p):
		if(self.errorStatus or p.sentenciaSecuencia is None):
			return
		else:
			p.sentenciaSecuencia.append(p.sentencia)
			return p.sentenciaSecuencia
		
	@_('sentencia')
	def sentenciaSecuencia(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSecuencia([p.sentencia])

	'''
	modulo : "MODULE" ID ";"
	declaracionTipoPuntoComa
	declaracionConstanteCONST
	declaracionVariableIN
	declaracionVariableINOUT
	declaracionVariableOUT
	declaracionVariableVAR
	declaracionRelacionPOS
	sentenciaSecuenciaBEGIN
	END ID "."
	;
	'''
	@_('MODULE ID ";" declaracionTipoPuntoComa declaracionConstanteCONST declaracionVariableIN declaracionVariableINOUT declaracionVariableOUT declaracionVariableVAR declaracionRelacionPOS sentenciaSecuenciaBEGIN END ID "."')
	def modulo(self, p):
		if(p.ID0!=p.ID1):
			print("error al definir modulo, no concuerda el ID {} {} con {} {} - Linea {}".format(p.MODULE, p.ID0, p.END, p.ID1, p.lineno))
			self.errorStatus=True
		elif(self.errorStatus):
			return
		else:
			return Modulo(p.ID0, p.declaracionTipoPuntoComa, p.declaracionConstanteCONST, p.declaracionVariableIN, p.declaracionVariableINOUT, p.declaracionVariableOUT, p.declaracionVariableVAR, p.declaracionRelacionPOS, p.sentenciaSecuenciaBEGIN, p.ID1)
		
	'''
	declaracionTipoPuntoComa : declaracionTipoPuntoComaR
	|	empty
	;
	'''	
	@_('declaracionTipoPuntoComaR')
	def declaracionTipoPuntoComa(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionTipoPuntoComa(p.declaracionTipoPuntoComaR)
	
	@_('empty')
	def declaracionTipoPuntoComa(self, p):
		return None
	'''
	declaracionTipoPuntoComaR : declaracionTipoPuntoComaR declaracionTipo ";"
	|	declaracionTipo ";"
	;
	'''
	@_('declaracionTipoPuntoComaR declaracionTipo ";"')
	def declaracionTipoPuntoComaR(self, p):
		if(self.errorStatus or p.declaracionTipoPuntoComaR is None):
			return
		else:
			p.declaracionTipoPuntoComaR.append(p.declaracionTipo)
			return p.declaracionTipoPuntoComaR
	
	@_('declaracionTipo ";"')
	def declaracionTipoPuntoComaR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionTipoPuntoComaR([p.declaracionTipo])
	
	'''
	declaracionConstanteCONST : "CONST" declaracionConstanteRecursivo
	|	empty
	;
	'''
	@_('CONST declaracionConstanteRecursivo')
	def declaracionConstanteCONST(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionConstanteCONST(p.declaracionConstanteRecursivo)
	
	@_('empty')
	def declaracionConstanteCONST(self, p):
		return None
	'''
	declaracionConstanteRecursivo : declaracionConstanteRecursivoR
	|	empty
	;
	'''
	@_('declaracionConstanteRecursivoR')
	def declaracionConstanteRecursivo(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionConstanteRecursivo(p.declaracionConstanteRecursivoR)
	
	@_('empty')
	def declaracionConstanteRecursivo(self, p):
		return None
	
	'''
	declaracionConstanteRecursivoR : declaracionConstanteRecursivoR declaracionConstante
	|	declaracionConstante
	;
	'''
	@_('declaracionConstanteRecursivoR declaracionConstante')
	def declaracionConstanteRecursivoR(self, p):
		if(self.errorStatus or p.declaracionConstanteRecursivoR is None):
			return
		else:
			p.declaracionConstanteRecursivoR.append(p.declaracionConstante)
			return p.declaracionConstanteRecursivoR
		
	@_('declaracionConstante')
	def declaracionConstanteRecursivoR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionConstanteRecursivoR([p.declaracionConstante])
	
	'''
	declaracionVariableIN : "IN" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('IN declaracionVariableRecursivo')
	def declaracionVariableIN(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableIN(p.declaracionVariableRecursivo)
	
	@_('empty')
	def declaracionVariableIN(self, p):
		return None
	
	
	'''
	declaracionVariableRecursivo : declaracionVariableRecursivoR
	|	empty
	;
	'''
	@_('declaracionVariableRecursivoR')
	def declaracionVariableRecursivo(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableRecursivo(p.declaracionVariableRecursivoR)
		
	@_('empty')
	def declaracionVariableRecursivo(self, p):
		return None
	
	'''
	declaracionVariableRecursivoR : declaracionVariableRecursivoR declaracionVariable
	|	declaracionVariable
	;
	'''
	@_('declaracionVariableRecursivoR declaracionVariable')
	def declaracionVariableRecursivoR(self, p):
		if(self.errorStatus or p.declaracionVariableRecursivoR is None):
			return
		else:
			p.declaracionVariableRecursivoR.append(p.declaracionVariable)
			return p.declaracionVariableRecursivoR
		
	@_('declaracionVariable')
	def declaracionVariableRecursivoR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableRecursivoR([p.declaracionVariable])
	
	'''
	declaracionVariableINOUT : "INOUT" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('INOUT declaracionVariableRecursivo')
	def declaracionVariableINOUT(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableINOUT(p.declaracionVariableRecursivo)
			
	@_('empty')
	def declaracionVariableINOUT(self, p):
		return None
		
	'''
	declaracionVariableOUT : "OUT" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('OUT declaracionVariableRecursivo')
	def declaracionVariableOUT(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableOUT(p.declaracionVariableRecursivo)
		
	@_('empty')
	def declaracionVariableOUT(self, p):
		return None
	
	'''
	declaracionVariableVAR : "VAR" declaracionVariableRecursivo
	|	empty
	;
	'''
	@_('VAR declaracionVariableRecursivo')
	def declaracionVariableVAR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionVariableVAR(p.declaracionVariableRecursivo)
	
	@_('empty')
	def declaracionVariableVAR(self, p):
		return None
	
	'''
	declaracionVariblePOS : POS declaracionRelacionRecursivo
	|	empty
	;
	'''
	@_('POS declaracionRelacionRecursivo')
	def declaracionRelacionPOS(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionRelacionPOS(p.declaracionRelacionRecursivo)
	
	@_('empty')
	def declaracionRelacionPOS(self, p):
		return None
	
	'''
	declaracionRelacionRecursivo :declaracionRelacionR
	|	empty
	;
	'''
	@_('declaracionRelacionR')
	def declaracionRelacionRecursivo(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionRelacionRecursivo(p.declaracionRelacionR)
		
	@_('empty')
	def declaracionRelacionRecursivo(self, p):
		return None
	
	'''
	declaracionRelacionR : declaracionRelacionR relacion ";"
	|	relacion ";"
	;
	'''
	
	@_('declaracionRelacionR relacion ";"')
	def declaracionRelacionR(self, p):
		if(self.errorStatus or p.declaracionRelacionR is None):
			return
		else:
			p.declaracionRelacionR.append(p.relacion)
			return p.declaracionRelacionR
		
	@_('relacion ";"')
	def declaracionRelacionR(self, p):
		if(self.errorStatus):
			return
		else:
			return DeclaracionRelacionR([p.relacion])
		
		
	'''
	sentenciaSecuenciaBEGIN : "BEGIN" sentenciaSecuencia
	|	empty
	;
	'''
	@_('BEGIN sentenciaSecuencia')
	def sentenciaSecuenciaBEGIN(self, p):
		if(self.errorStatus):
			return
		else:
			return SentenciaSecuenciaBEGIN(p.sentenciaSecuencia)

	@_('empty')
	def sentenciaSecuenciaBEGIN(self, p):
		return None
		
	'''
	tipoFormal : expresionCorcheteO "BIT"
	;
	'''
	@_('expresionCorcheteO BIT')
	def tipoFormal(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormal(p.expresionCorcheteO)
		
	'''
	expresionCorcheteO : expresionCorcheteOR
	|	empty
	;
	'''
	@_('expresionCorcheteOR')
	def expresionCorcheteO(self, p):
		if(self.errorStatus):
			return
		else:
			return ExpresionCorcheteO(p.expresionCorcheteOR)
	
	@_('empty')
	def expresionCorcheteO(self, p):
		return None
	
	
	'''
	expresionCorcheteOR : expresionCorcheteOR "[" expresionOpcional "]"
	|	"[" expresionOpcional "]"
	;
	'''
	@_('expresionCorcheteOR "[" expresionOpcional "]"')
	def expresionCorcheteOR(self, p):
		if(self.errorStatus or p.expresionCorcheteOR is None):
			return
		else:
			p.expresionCorcheteOR.append(p.expresionOpcional)
			return p.expresionCorcheteOR
		
	@_('"[" expresionOpcional "]"')
	def expresionCorcheteOR(self, p):
		if(self.errorStatus):
			return
		else:
			return ExpresionCorcheteOR([p.expresionOpcional])
	
	'''
	expresionOpcional : expresion
	|	empty
	;
	'''
	@_('expresion')
	def expresionOpcional(self, p):
		if(self.errorStatus):
			return
		else:
			return ExpresionOpcional(p.expresion)
	
	@_('empty')
	def expresionOpcional(self, p):
		return None
	
	
	'''
	tipoFormalBus : expresionCorcheteO "TS"
	|	expresionCorcheteO "OC"
	;
	'''
	@_('expresionCorcheteO TS', 
	'expresionCorcheteO OC')
	def tipoFormalBus(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormalBus(p[0], p[1])
		
	'''
	declaracionTipo : "TYPE" ID simboloPor listaIdParentesis ";" 
	declaracionConstanteCONST 
	tipoFormalIN
	tipoFormalINOUT
	declaracionVariableOUT 
	declaracionVariableVAR 
	sentenciaSecuenciaBEGIN 
	END ID
	;
	'''
	@_('TYPE ID simboloPor listaIdParentesis ";" declaracionConstanteCONST tipoFormalIN tipoFormalINOUT declaracionVariableOUT declaracionVariableVAR declaracionRelacionPOS sentenciaSecuenciaBEGIN END ID')
	def declaracionTipo(self, p):
		if(p.ID0!=p.ID1):
			print("error el {} {} no coincide con su nombre de identificador {} {}".format(p.TYPE, p.ID0, p.END, p.ID1))
			self.errorStatus=True
		elif(self.errorStatus):
			return
		else:
			return DeclaracionTipo(p.ID0, p.simboloPor, p.listaIdParentesis, p.declaracionConstanteCONST, p.tipoFormalIN, p.tipoFormalINOUT, p.declaracionVariableOUT, p.declaracionVariableVAR, p.declaracionRelacionPOS, p.sentenciaSecuenciaBEGIN, p.ID1)
	
	
	'''
	simboloPor : "*"
	|	empty
	;
	'''
	@_('"*"')
	def simboloPor(self, p):
		if(self.errorStatus):
			return
		else:
			return p[0]
		
	@_('empty')
	def simboloPor(self, p):
		return None
		
	'''
	listaIdParentesis : "(" listaId ")"
	|	empty
	;
	'''
	@_('"(" listaId ")"')
	def listaIdParentesis(self, p):
		if(self.errorStatus):
			return
		else:
			return ListaIdParentesis(p.listaId)
		
	@_('empty')
	def listaIdParentesis(self, p):
		return None
		
	'''
	tipoFormalIN : IN tipoFormallistaId
	|	empty
	;
	'''
	@_('IN tipoFormallistaId')
	def tipoFormalIN(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormalIN(p.tipoFormallistaId)
		
	@_('empty')
	def tipoFormalIN(self, p):
		return None
		
	'''
	tipoFormallistaId : tipoFormallistaIdR 
	|	empty
	;
	'''
	@_('tipoFormallistaIdR')
	def tipoFormallistaId(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormallistaId(p.tipoFormallistaIdR)
		
	@_('empty')
	def tipoFormallistaId(self, p):
		return None
		
	'''
	tipoFormallistaIdR : tipoFormallistaIdR listaId ":" tipoFormal ";"
	|	listaId ":" tipoFormal ";"
	;
	'''
	@_('tipoFormallistaIdR listaId ":" tipoFormal ";"')
	def tipoFormallistaIdR(self, p):
		if(self.errorStatus or p.tipoFormallistaIdR is None):
			return
		else:
			p.tipoFormallistaIdR.append(p.listaId, p.tipoFormal)
			return p.tipoFormallistaIdR
		
	@_('listaId ":" tipoFormal ";"')
	def tipoFormallistaIdR(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormallistaIdR([p.listaId],[p.tipoFormal])

	'''
	tipoFormnalINOUT : INOUT tipoFormlBuslistaId
	|	empty
	;
	'''
	@_('INOUT tipoFormlBuslistaId')
	def tipoFormalINOUT(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormalINOUT(p.tipoFormlBuslistaId)
		
	@_('empty')
	def tipoFormalINOUT(self, p):
		return None
		
	'''
	tipoFormlBuslistaId : tipoFormlBuslistaIdR
	|	empty
	;
	'''
	@_('tipoFormlBuslistaIdR')
	def tipoFormlBuslistaId(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormlBuslistaId(p.tipoFormlBuslistaIdR)
		
	@_('empty')
	def tipoFormlBuslistaId(self, p):
		return None
	
	'''
	tipoFormlBuslistaIdR : tipoFormlBuslistaIdR listaId ":" tipoFormalBus ";"
	|	listaId ":" tipoFormalBus ";"
	;
	'''
	@_('tipoFormlBuslistaIdR listaId ":" tipoFormalBus ";"')
	def tipoFormlBuslistaIdR(self, p):
		if(self.errorStatus or p.tipoFormlBuslistaIdR is None):
			return
		else:
			p.tipoFormlBuslistaIdR.append(p.listaId, p.tipoFormalBus)
			return p.tipoFormlBuslistaIdR
		
	@_('listaId ":" tipoFormalBus ";"')
	def tipoFormlBuslistaIdR(self, p):
		if(self.errorStatus):
			return
		else:
			return TipoFormlBuslistaIdR([p.listaId], [p.tipoFormalBus])
	'''
	assinacionUnidad : ID selector "(" listaExpresiones ")"
	'''
	@_('ID selector "(" listaExpresiones ")"')
	def asignacionUnidad(self, p):
		if(self.errorStatus):
			return
		else:
			return AsignacionUnidad(p.ID, p.selector, p.listaExpresiones)
	
	'''
	empty :
	'''
	@_('')
	def empty(self, p):
		return None
	
	#prueba de errores
	'''
	tipoSimple : tipoBasico
		|	ID "(" listaExpresiones ")"
		|	ID
		;
	'''
	# @_('error') 
	# def tipoSimple(self, p):
		# print("error al indicar tipo simple en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	tipoBasico : 'BIT'
		| 'TS'
		| 'OC'
		;
	'''
	@_('error')
	def tipoBasico(self, p):
		print("error al indicar el tipo basico en {} - linea {}, debe ser BIT TS o OC".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
		
	'''
	listaExpresiones : listaExpresiones "," expresion
		| expresion
		;
	'''
	# @_('error')
	# def listaExpresiones(self, p):
		# print("error al formar la lista de expresiones en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
		
	'''
	tipo : "[" expresion "]" tipo
		|	tipoSimple
		;
	'''
	# @_('error')
	# def tipo(self, p):
		# print("error al formar tipo en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# pass
		
	
	'''
	declaracionConstante : ID DOSPUNTOSIGUAL expresion ";"'
	|	error
	;
	'''
	@_('error')
	def declaracionConstante(self, p):
		print("error al declarar constante en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
	
	'''
	declaracionVariable : listaId ":" tipo ";"
	;
	'''
	@_('listaId error')
	def declaracionVariable(self, p):
		print("error al declarar variable en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
	
	'''
	listaId : listaId "," ID
		|	ID
		|	error
		;
	'''
	@_('error')
	def listaId(self, p):
		print("error con la lista de ID en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
	
	'''
	selector : selectorR
	|	empty
	;
	'''
	'''
	@_('error')
	def selectorR(self, p):
		print("error al indicar selector en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
	'''
		
	'''
	factor : ID selector
	|	valorLogico
	|	INTEGER
	|	"~" factor
	|	"?" factor
	|	'FLECHAARRIBA factor'
	|	"(" expresion ")"
	|	"MUX" "(" expresion ":" expresion "," expresion ")"
	|	"MUX" "(" expresion "," expresion ":" expresion "," expresion "," expresion "," expresion)
	|	"REG" "(" expresion ")"
	|	"REG" "(" expresion "," expresion ")"
	|	"LATCH" "(" expresion "," expresion ")"
	|	"SR" "(" expresion "," expresion ")"
	;
	'''
	#'"↑" factor', genera error de enconding
	# @_('error')
	# def factor(self, p):
		# print("error en declaración de factor en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# pass
		
	'''
	termino : termino simbolosProd factor
	|	factor
	;
	'''	
	
	@_('error factor')
	def termino(self, p):
		print("error al declarar termino en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
		
	'''
	simbolosProd : "*"
	|	"/"
	|	"DIV"
	|	"MOD"
	;
	'''
	# @_('error')
	# def simbolosProd(self, p):
		# print("error en los simbolos de termino en {} se esperaba * / DIV MOD - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	
	'''
	expresion : expresion "+" termino
	|	expresion "-" termino
	|	termino
	;
	'''
	# @_('error')
	# def expresion(self, p):
		# print("error al declarar expresion en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	asignacion : ID selector DOSPUNTOSIGUAL expresion
	|	ID selector DOSPUNTOSIGUAL condicion "|" expresion
	;
	'''
	# @_('error')
	# def asignacion(self, p):
		# print("error al hacer asignación en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	condicion : expresion
	;
	'''
	# @_('error')
	# def condicion(self, p):
		# print("error de la condición en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	relacion : expresion "=" expresion
	|	expresion "#" expresion
	|	expresion "<" expresion
	|	expresion MENORIGUAL expresion
	|	expresion ">" expresion
	|	expresion MAYORIGUAL expresion
	;
	'''
	# @_('error')
	# def relacion(self, p):
		# print("error al efectuar relación en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	sentenciaSi : "IF" relacion "THEN" sentenciaSecuencia sentenciaSiSino sentenciaSiEntonces "END"
	;
	'''
	# @_('error')
	# def sentenciaSi(self, p):
		# print("error declarando el if en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	sentenciaSiSino : sentenciaSiSinoR
	|	empty
	;
	'''
	# @_('error')
	# def sentenciaSiSino(self, p):
		# print("error al declarar el elsif en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass

	'''
	sentenciaSiEntonces : "ELSE" sentenciaSecuencia
	|	empty
	;
	'''
	# @_('error')
	# def sentenciaSiEntonces(self, p):
		# print("error al declarar else en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	sentenciaPara : "FOR" ID ":=" expresion DOBLEPUNTO expresion "DO" sentenciaSecuencia "END"
	;
	'''
	# @_('error')
	# def sentenciaPara(self, p):
		# print("error al declarar el for en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	sentencia : asignacion
	|	asignacionUnidad
	|	sentenciaSi
	|	sentenciaPara
	|	empty
	;
	'''
	# @_('error')
	# def sentencia(self, p):
		# print("error al declrar la sentencia en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass

	'''
	modulo : MODULE ID ";"
	declaracionTipoPuntoComa
	declaracionConstanteCONST
	declaracionVariableIN
	declaracionVariableINOUT
	declaracionVariableOUT
	declaracionVariableVAR
	sentenciaSecuenciaBEGIN
	END ID "."
	;
	'''
	@_('MODULE ID ";" error')
	def modulo(self, p):
		print("error al declarar MODULO {} en {} - Line {}".format(p.ID, p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass 
	
	'''
	declaracionTipoPuntoComaR : declaracionTipoPuntoComaR declaracionTipo ";"
	|	declaracionTipo ";"
	;
	'''
	# @_('error')
	# def declaracionTipoPuntoComaR(self, p):
		# print("error al decalrar TYPE'S en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	declaracionConstanteCONST : "CONST" declaracionConstanteRecursivo
	|	empty
	
	'''
	# @_('error')
	# def declaracionConstanteCONST(self, p):
		# print("error al declarar constante de un MODULO en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	declaracionConstanteRecursivo : declaracionConstanteRecursivoR
	|	empty
	;
	'''
	# @_('declaracionConstanteRecursivoR',
	# 'empty')
	# def declaracionConstanteRecursivo(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	declaracionConstanteRecursivoR : declaracionConstanteRecursivoR declaracionConstante
	|	declaracionConstante
	;
	'''
	# @_('error')
	# def declaracionConstanteRecursivoR(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	declaracionVariableIN : "IN" declaracionVariableRecursivo
	|	empty
	;
	'''
	# @_('error')
	# def declaracionVariableIN(self, p):
		# print("error al declarar variable de entrada de un MODULO en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	declaracionVariableRecursivo : declaracionVariableRecursivoR
	|	empty
	;
	'''
	# @_('error')
	# def declaracionVariableRecursivo(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	declaracionVariableRecursivoR : declaracionVariableRecursivoR declaracionVariable
	|	declaracionVariable
	;
	'''
	# @_('error')
	# def declaracionVariableRecursivoR(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	declaracionVariableINOUT : "INOUT" declaracionVariableRecursivo
	|	empty
	;
	'''
	# @_('error')
	# def declaracionVariableINOUT(self, p):
		# print("error al declrar entrada/salida de un MODULO en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	declaracionVariableOUT : "OUT" declaracionVariableRecursivo
	|	empty
	;
	'''
	# @_('error')
	# def declaracionVariableOUT(self, p):
		# print("error al declarar variable de salida en {} - linea".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	declaracionVariableVAR : "VAR" declaracionVariableRecursivo
	|	empty
	;
	'''
	# @_('error')
	# def declaracionVariableVAR(self, p):
		# print("error al declarar variable VAR en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	declaracionVariblePOS : POS declaracionRelacionRecursivo
	|	empty
	;
	'''
	# @_('error')
	# def declaracionVariblePOS(self, p):
		# print("error al declarar variable POS de un MODULO en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	declaracionRelacionRecursivo :declaracionRelacionRecursivo relacion ";"
	|	relacion ";"
	;
	'''
	# @_('error')
	# def declaracionRelacionRecursivo(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	sentenciaSecuenciaBEGIN : "BEGIN" sentenciaSecuencia
	|	empty
	;
	'''
	# @_('error')
	# def sentenciaSecuenciaBEGIN(self, p):
		# print("error al declarar BEGIN en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass

	'''
	tipoFormal : expresionCorcheteO "BIT"
	;
	'''
	@_('error')
	def tipoFormal(self, p):
		print("error al declrar tipo forma en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
		
	'''
	expresionCorcheteO : expresionCorcheteOR
	|	empty
	;
	'''
	# @_('error')
	# def expresionCorcheteO(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	expresionCorcheteOR : expresionCorcheteOR "[" expresionOpcional "]"
	|	"[" expresionOpcional "]"
	;
	'''
	# @_('error')
	# def expresionCorcheteOR(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	expresionOpcional : expresion
	|	empty
	;
	'''
	# @_('error')
	# def expresionOpcional(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	tipoFormalBus : expresionCorcheteO "TS"
	|	expresionCorcheteO "OC"
	;
	'''
	@_('error')
	def tipoFormalBus(self, p):
		print("error al declarar bus de datos formal en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
		
	'''
	declaracionTipo : "TYPE" ID simboloPor listaIdParentesis ";" 
	declaracionConstanteCONST 
	tipoFormalIN
	tipoFormlINOUT
	declaracionVariableOUT 
	declaracionVariableVAR 
	sentenciaSecuenciaBEGIN 
	END ID
	;
	'''
	@_('TYPE ID error')
	def declaracionTipo(self, p):
		print("error al declarar el TYPE {} en {} - linea {}".format(p.ID, p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
	
	'''
	simboloPor : "*"
	|	empty
	;
	'''
	# @_('error')
	# def simboloPor(self, p):
		# print("error se esperaba un * o vacio al declarar un TYPE en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	listaIdParentesis : "(" listaId ")"
	|	empty
	;
	'''
	# @_('error')
	# def listaIdParentesis(self, p):
		# print("error se esperaba una lista de identificadores o vacio al declarar un TYPE en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	tipoFormalIN : IN tipoFormallistaId
	|	empty
	;
	'''
	# @_('error')
	# def tipoFormalIN(self, p):
		# print("error al declarar entrada de datos de TYPE en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	tipoFormallistaId : tipoFormallistaIdR 
	|	empty
	;
	'''
	# @_('error')
	# def tipoFormallistaId(self, p):
		# print("")
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	tipoFormallistaIdR : tipoFormallistaIdR listaId ":" tipoFormal ";"
	|	listaId ":" tipoFormal ";"
	;
	'''
	# @_('error')
	# def tipoFormallistaIdR(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass

	'''
	tipoFormnalINOUT : INOUT tipoFormlBuslistaId
	|	empty
	;
	'''
	# @_('error')
	# def tipoFormlINOUT(self, p):
		# print("error al declarar entrada/salida de TYPE en {} - linea {}".format(p.error.value, p.error.lineno))
		# self.errorStatus=True
		# self.errok()
		# pass
		
	'''
	tipoFormlBuslistaId : tipoFormlBuslistaIdR
	|	empty
	;
	'''
	# @_('error')
	# def tipoFormlBuslistaId(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass
	
	'''
	tipoFormlBuslistaIdR : tipoFormlBuslistaIdR listaId ":" tipoFormalBus ";"
	|	listaId ":" tipoFormalBus ";"
	;
	'''
	# @_('error')
	# def tipoFormlBuslistaIdR(self, p):
		# self.errorStatus=True
		# self.errok()
		# pass

	'''
	assinacionUnidad : ID selector "(" listaExpresiones ")"
	'''
	@_('error')
	def asignacionUnidad(self, p):
		print("error al asignar unidad en {} - linea {}".format(p.error.value, p.error.lineno))
		self.errorStatus=True
		self.errok()
		pass
	
	def error(self, p):
		self.errorStatus=True
		if p:
			#print("Syntax error at token", p.type)
			# Just discard the token or tell the parser it's okay.
			self.errok()
		else:
			print("Syntax error at EOF")
		pass
		
		#pass
def parse(data, debug=0):
	#print(parser.error)
	p = parser.parse(lexer.tokenize(data))
	#print(parser.errorStatus)
	if parser.errorStatus:
		print("error en codigo")
		return None
	print("sin errores\n")
	return p
		
if __name__ == '__main__':
	import sys
	lexer = CalcLexer()
	parser = CalcParser()
	if(len(sys.argv)!=2):#Verifica la cantidad de argumentos a la hora de compilar si no son 2. "py 'fichero.py' 'archivo'"
		sys.stderr.write('Usage: "{}" "filename"\n'.format(sys.argv[0]))#permite que al al compilar indique que debe de darse el archivo de la forma python.exe "fichero.py" "Archivo a abrir, como un simple print"
		raise SystemExit(1)#termina el programa
	file= open(sys.argv[1]).read()#en caso de que indique archivo tome el segundo string y abra el archivo y convierta con .read() a string
	"""
	maxLenthLine=0
	for linea in open(sys.argv[1]):
		if(maxLenthLine<len(linea)):
			maxLenthLine=len(linea)#verifica la columna maxima para el formato de centrado (visual en los print)
			print("malen",maxLenthLine)
	print("{:{align}{width}}".format("Archivo recibido - contenido inicio", align="^", width=maxLenthLine))
	print("-"*maxLenthLine)
	print(file)
	print("-"*maxLenthLine)
	print("{:{align}{width}}".format("Archivo recibido - contenido fin", align="^", width=maxLenthLine))
	"""
	#print("aplicando tokenize")
	lexer.fileName=sys.argv[1]
	
	#parse(file).pprint()
	p=parse(file)
	
	dot=DotCode()
	dot.visit(p)
	if(not dot.errorStatus and p is not None):
		gen=GenerateCode()
		gen.visit(p)
		for enum, code in enumerate(gen.code):
			print(enum,code)
	else:
		print("Se han presentado errores en los analisis anteriores")
	
	
	
	#print(dot.__repr__)
	#top = parse(file)
	#for item in flatten(top):
	#	print(item)
	