# CarFord

- [Instalação](#instalação)
  - [Usando Docker](#usando-Docker)
  - [Usando ambiente virtual](#usando-ambiente-virtual)
  - [Instalação das Dependências ](#instalação-das-dependências)
- [Rodar Projeto](#rodar-projeto)
- [Cobertura de Testes](#cobertura-de-testes)
- [Documentação](#documentaç)
- [Front end do projeto(em construção)](#frontend)



## Instalação

### Clonar repositório
```
https://github.com/wascellys/carford-challenge.git
```

## Usando Docker
Na raiz do projeto, abra o terminal e execute o comando  
```
docker-compose up --build
```

## Usando ambiente virtual
#### Instalação do Python em terminal Linux
```
sudo apt install python3-pip python3-dev libpq-dev virtualenv
```
#### Criando virtualenv
```
virtualenv myenv --python=python3
```
#### Ativação da  virtualenv
```
source myenv/bin/activate
```
## Instalação das Dependências
```
pip install -r requirements.txt
```
## Criar banco de dados
```
psql -h localhost -U postgres
```

#### Criar banco de dados
```
CREATE DATABASE carford-db;

GRANT ALL ON DATABASE carford-db TO postgres;
```

## Rodar Projeto
No diretório raiz do projeto execute o comando:
```
flask --app app --debug run --host=0.0.0.0
```

## Cobertura de testes
No diretório do projeto execute o comando:
```
coverage run -m pytest
```

Para ver os testes em detalhe, execute o comando:
```
coverage report -m
```

Para gerar um relatório com os testes em um arquivo HTML, execute o comando:
```
coverage html
```
Será criada uma nova pasta com o nome "htmlcov", basta abrir no arquivo index.html no navegador.

## Documentação
## Requisições HTTP
Toda requisição para a API são feitas por uma requisição HTTP usando para um dos seguintes métodos:

* `POST` Criar um recurso
* `PUT` Atualizar um recurso
* `GET` Buscar um ou uma lista de recursos
* `DELETE` Excluir um recurso

## Códigos de respostas HTTP
Cada resposta será retornada com um dos seguintes códigos de status HTTP:

* `201` `CREATED` A criação foi bem sucedida
* `200` `OK` A requisição foi bem sucedida
* `400` `Bad Request` Houve um problema com a solicitação (segurança, malformado, validação de dados, etc.)
* `401` `Unauthorized` As credenciais fornecidas à API são inválidas
* `403` `Forbidden` As credenciais fornecidas não têm permissão para acessar o recurso solicitado
* `404` `Not found` Foi feita uma tentativa de acessar um recurso que não existe
* `500` `Server Error` Ocorreu um erro no servidor

## Endpoints

### Endpoints abetos
Os endpoints abertos não precisam de autenticação :

- *[Login]() : `POST` `/api/login`*
- *[Register]() : `POST` `/api/register`*

#### Login e Register
- Campos:
  | Campo     | Descição        | Tipo    | Obrigatório             |
  | :----     | :------         | :------ | :---------------------: |
  | username  | Nome de usuario | String  | :ballot_box_with_check: |
  | email     | Email do usuário | String  | :ballot_box_with_check: |
  | password  | Senha do usuário | String  | :ballot_box_with_check: |
  | name  | Nome do usuário | String  | :ballot_box_with_check: |

- Rotas
  - *Cadastrar usuário: `POST` `/register`*
  - *Obter token de autenticação: `POST` `/login`*
  

### Endpoints fechados
Os endpoints fechados precisam de autenticação via token:
passar no cabeçalho da requisição: "Authorization": Bearer <token>

#### Carro (Car)


- Campos:
  | Campo       | Descição                       | Tipo     | Obrigatório             |
  | :----       | :------                        | :------  | :---------------------: |
  | name      | Nome do carro        | String  | :ballot_box_with_check: |
  | model | Modelo do carro         | String   | :ballot_box_with_check: |
  | color      | Cor do carro          | String   | :ballot_box_with_check: |
  | owner_id        | código do proprietário do carro | String   | :ballot_box_with_check: |

- Rotas
  - *Listar carros: `GET` `/v1/cars`*
  - *Cadastrar um carro: `POST` `/v1/cars`*
  - *Atualizar um os dados de um carro: `PUT` `/v1/cars/{id}`*
  - *Deletar um carro cadastrado: `DELETE` `/v1/cars/{id}/`*
  
  OBS: Ao cadastrar um carro deve ser informado um modelo (model) e uma cor ( color), e devem ser escolhidas umas das seguintes opções,
  obrigatóriamente:
  - MODELO: "Hatch", "Sedan" ou "Convertible"
  - COR: "Blue", "Gray" e "Yellow"

  Qualquer outra opção, diferente dessas, gerará erro na requisiç


#### Proprietario (Owner)


- Campos:
  | Campo       | Descição                       | Tipo     | Obrigatório             |
  | :----       | :------                        | :------  | :---------------------: |
  | name      | Nome do proprietário        | String  | :ballot_box_with_check: |

- Rotas
  - *Listar proprietarios: `GET` `/v1/owners`*
  - *Cadastrar um proprietário: `POST` `/v1/owners`*
  - *Atualizar um proprietário cadastrado: `PUT` `/v1/owners/{id}`*
  - *Deletar um proprietário cadastrado: `DELETE` `/v1/owners/{id}/`*
  
## Front end
  
  <Em construção>

