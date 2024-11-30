const formImc = document.querySelector('.form');
const resposta = document.querySelector('.resposta');



formImc.addEventListener('submit', (event) => {
    event.preventDefault(); // Impede o comportamento padrão

    const peso = document.querySelector('.peso').value;
    const altura = document.querySelector('.altura').value;

    let isNumeroPeso = isNaN(Number(peso));
    let isNumeroAltura = isNaN(Number(altura));


    if (isNumeroPeso && isNumeroAltura) {
        resposta.innerHTML = 'Dados de PESO E ALTURA incorreto, insira somente números.'
    } else if (isNumeroPeso) {
        resposta.innerHTML = 'Dados de PESO incorreto, insira somente números e pontos.'
    } else if (isNumeroAltura) {
        resposta.innerHTML = 'Dados de ALTURA incorreto, insira somente números e pontos.'
    } else {
        resposta.innerHTML = ''
    }

    //calculo de imc
    let imc = Number(peso) / (Number(altura) ** 2)

    if (imc < 18.5) {
        resposta.innerHTML = `Seu IMC é ${imc.toFixed(1)} é Abaixo do peso`;
    } else if (imc >= 18.5 && imc <= 24.9) {
        resposta.innerHTML = `Seu IMC é ${imc.toFixed(1)} é Peso Normal`;
    } else if (imc >= 25 && imc <= 29.9) {
        resposta.innerHTML = `Seu IMC é ${imc.toFixed(1)} é Sobrepeso`;
    } else if (imc >= 30 && imc <= 34.9) {
        resposta.innerHTML = `Seu IMC é ${imc.toFixed(1)} é Obsidade grau 1`;
    } else if (imc >= 35 && imc <= 39.9) {
        resposta.innerHTML = `Seu IMC é ${imc.toFixed(1)} é Obsidade grau 2`;
    } else if (imc >= 40) {
        resposta.innerHTML = `Seu IMC é ${imc.toFixed(1)} é Obsidade grau 3`;
    } else {
        resposta.innerHTML = `Erro ao Calcular, Digite Corretamente os dados!`;

    }

});











