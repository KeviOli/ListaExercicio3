import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Definindo o nome do arquivo JSON para armazenar os produtos
produtos_file = 'produtos.json'

# Função para verificar se o arquivo JSON existe e criá-lo se não existir
def criar_arquivo_produtos():
    if not os.path.exists(produtos_file):
        with open(produtos_file, 'w') as file:
            json.dump([], file)

# Função para carregar os produtos do arquivo JSON
def carregar_produtos():
    criar_arquivo_produtos()
    with open(produtos_file, 'r') as file:
        produtos = json.load(file)
    return produtos

# Função para salvar os produtos no arquivo JSON
def salvar_produtos(produtos):
    with open(produtos_file, 'w') as file:
        json.dump(produtos, file, indent=4)

# Rota para listar todos os produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = carregar_produtos()
    return jsonify(produtos)

# Rota para adicionar um novo produto
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    novo_produto = request.json
    produtos = carregar_produtos()
    
    # Atribuir um ID único para o novo produto
    novo_produto['id'] = len(produtos) + 1
    
    produtos.append(novo_produto)
    salvar_produtos(produtos)
    return jsonify(novo_produto), 201

# Rota para atualizar o estoque de um produto
@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_estoque(produto_id):
    produtos = carregar_produtos()
    for produto in produtos:
        if produto['id'] == produto_id:
            produto['estoque'] = request.json['estoque']
            salvar_produtos(produtos)
            return jsonify(produto)
    return jsonify({'mensagem': 'Produto não encontrado'}), 404

# Rota para deletar um produto
@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    produtos = carregar_produtos()
    for produto in produtos:
        if produto['id'] == produto_id:
            produtos.remove(produto)
            salvar_produtos(produtos)
            return jsonify({'mensagem': 'Produto deletado'})
    return jsonify({'mensagem': 'Produto não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
