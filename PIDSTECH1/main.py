#!/usr/bin/env python3
"""
PIDS TECH - Sistema de Gerenciamento de Componentes
Arquivo principal do sistema

Autor: Sistema PIDS TECH
Versão: 2.0
Data: 2025
"""

import sys
import os

def main():
    """Função principal do sistema"""
    try:
        print("🚀 Iniciando PIDS TECH - Sistema de Componentes...")
        print("📱 Carregando interface moderna...")
        
        # Carregar interface moderna diretamente
        from interface_moderna import PidsTechModerna
        app = PidsTechModerna()
        app.executar()
        
    except KeyboardInterrupt:
        print("\n⚠️ Sistema interrompido pelo usuário.")
        sys.exit(0)
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("💡 Certifique-se de que todos os arquivos estão no mesmo diretório.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro crítico no sistema: {e}")
        sys.exit(1)
    finally:
        print("👋 Sistema PIDS TECH encerrado.")

def verificar_dependencias():
    """Verifica se todas as dependências estão disponíveis"""
    dependencias = {
        'tkinter': 'Interface gráfica',
        'sqlite3': 'Banco de dados'
    }
    
    dependencias_faltando = []
    
    for modulo, descricao in dependencias.items():
        try:
            __import__(modulo)
        except ImportError:
            dependencias_faltando.append(f"{modulo} ({descricao})")
    
    if dependencias_faltando:
        print("❌ Dependências não encontradas:")
        for dep in dependencias_faltando:
            print(f"   - {dep}")
        print("\n💡 Para instalar tkinter no Ubuntu/Debian:")
        print("   sudo apt-get install python3-tk")
        return False
    
    return True

def verificar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    arquivos_necessarios = [
        'database.py',
        'interface_moderna.py'
    ]
    
    arquivos_faltando = []
    
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            arquivos_faltando.append(arquivo)
    
    if arquivos_faltando:
        print("❌ Arquivos não encontrados:")
        for arquivo in arquivos_faltando:
            print(f"   - {arquivo}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🏢 PIDS TECH - Sistema de Gerenciamento de Componentes v2.0")
    print("=" * 60)
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("❌ Sistema não pode ser executado devido a arquivos faltando.")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    # Verificar dependências
    if not verificar_dependencias():
        print("❌ Sistema não pode ser executado devido a dependências faltando.")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    # Executar aplicação
    main()