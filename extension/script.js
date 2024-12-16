const botao = document.querySelector('button');
const span = document.querySelector('.resposta');
const input = document.querySelector('input')




const pegarTitulosEUrl = () => {
    function criarLinkDownload(array, url) {


        const arrayDoTitulo = array;
        const urlDaPaginaAtiva = url;

        let conteudo;

        conteudo = `\nLINK: ${url}\n\n\n`;

        arrayDoTitulo.forEach(item => {
            conteudo += `${item.tag.toUpperCase()}: ${item.texto}\n`;
        });






        const blob = new Blob([conteudo], { type: 'text/plain' });

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'meuarquivo.txt';  // Nome do arquivo que será baixado

        link.click();
    }


    const titulos = [];
    const tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'];
    const url = window.location.href;

    tags.forEach(tag => {
        const elementos = document.querySelectorAll(tag);

        elementos.forEach(elemento => {
            titulos.push({ tag, texto: elemento.innerText })
        });
    })


    criarLinkDownload(titulos, url);

}



botao.addEventListener('click', async function (e) {
    e.preventDefault();
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });


    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: pegarTitulosEUrl,
    });
});




