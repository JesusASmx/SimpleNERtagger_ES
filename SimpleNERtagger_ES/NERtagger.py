import re

#NER tagger en español versión 1.
#Por: Jesús Armenta-Segura. CIC-IPN, IFE:LL&DH@ITESM
#Por ahora sólo enmascara, y únicamente lidia con teléfonos y direcciones de correo electrónico.
#En la versión 2 se incluirá un tagger con BERT para nombres, objetos y lugares.
#En la versión 3 se incluirá ollama para taggear puestos, hora/momento y relaciones interpersonales.
class NER_tagger:
  def __init__(self):
    return

  def quitar_emails(self, text, tag):
    #Construcción de la gramática Backus-Naur que genera (casi) todos los emails del mundo.
    DOM = r"[a-zA-Z0-9-_àèìòùäëïöüáéíóúç+*]+"     # DOM  ::= Dominio de internet. Puede ser tan simple como "yahoo", o tan complicado como "deez-natz-funny". El TLD es considerado más adelante.
    USER = r"[a-zA-Z0-9-_àèìòùäëïöüáéíóúç+*.]+"   # USER ::= Algún string sin caracteres raros.
    email_regex = USER+r"@"+DOM                   # email_regex ::= USER @ DOM

    pattern = re.compile(email_regex)

    matches = pattern.findall(text)

    for match in matches:
      text = text.replace(match, tag+"@@@") #Triple arroba es útil para marcar, porque no es una cadena que se encuentre fácilmente en las junglas de textos.

    # En caso de que sí se haya incluído algún TLD, lo removemos:
    inner_TLD = r"@@@\.[a-zA-Z0-9-_àèìòùäëïöüáéíóúç+*]+(?:\.[a-zA-Z0-9-_àèìòùäëïöüáéíóúç+*]+)*"

    TLD_pattern = re.compile(inner_TLD)
    TLDs = set(TLD_pattern.findall(text)) #TLD's, pero sólo los que van precedidos por el tag, marcado con @@@.
    for tld in TLDs:
      text = text.replace(tld, "")
  
    return text.replace("@@@", "") #Removemos el tag auxiliar @@@.


  def quitar_telefonos(self, text, tag):
    TEL = r"[0-9 -+]{6,}" #Números, pudiendo estar separados por espacios o guiones medios. Se incluye el + para casos como "+52".
    pattern = re.compile(TEL)

    NUM = r"[0-9]"
    num_pattern = re.compile(NUM) #Esto nos permitirá contar los números en el string rescatado, y evitar taggear como teléfono una secuencia aleatoria de espacios.
    matches = [x for x in pattern.findall(text) if len(num_pattern.findall(x)) > 5] #len > 5 porque consideramos el caso minimal 12345678, con ocho números. De ahí, consideramos versiones mutiladas, por ejemplo con 6 números, para estar seguros.

    for match in matches:
      text = text.replace(match, " "+tag+" ")

    return text


  def enmascarar(self, texto, mails_tag, tels_tag):
    if mails_tag:
      texto = self.quitar_emails(texto, str(mails_tag))
    if tels_tag:
      texto = self.quitar_telefonos(texto, str(tels_tag))
    return texto
