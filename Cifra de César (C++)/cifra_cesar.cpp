#include <iostream>
#include <fstream>
#include <string>

using namespace std;

string ler_arquivo(string diretorio) {
    
    string texto = "";

    ifstream arquivo;
    arquivo.open(diretorio, ios::in);
    
    if(arquivo.is_open()) {
        while(!arquivo.eof()){
            string linha;
            getline(arquivo,linha);
            texto += linha + "\n";
        }
        texto.pop_back();
        arquivo.close();
    } else {
        cout << "Erro ao abrir o arquivo" << endl;
    }
    return texto;
}

string cifrar_cesar(string texto_claro, int deslocamento){
    for(int i = 0; i < texto_claro.size(); i++){
        int  aux = texto_claro.at(i) + deslocamento;
        if(aux > 255){
            aux %= 255; 
        }
        texto_claro[i] = char(aux);
    }
    return texto_claro;
}

string decifrar_cesar(string texto_cifrado, int deslocamento){
    for(int i = 0; i < texto_cifrado.size(); i++){
        int  aux = texto_cifrado.at(i) - deslocamento;
        if(aux < 0){
            aux += 255; 
        }
        texto_cifrado[i] = char(aux);
    }
    return texto_cifrado;
}

int main(int argc, char **argv)
{
    string texto_claro = ler_arquivo("texto-claro.txt");
    cout << texto_claro << endl;

    string texto_cifrado = cifrar_cesar(texto_claro, 3);
    cout << texto_cifrado << endl;

    string texto_decifrado = decifrar_cesar(texto_cifrado, 3);
    cout << texto_decifrado << endl;
}