document.querySelectorAll('.menu-item, .submenu-item').forEach(item => {
    item.addEventListener('click', event => {
        const content = document.querySelector('.content');
        content.innerHTML = `<p>Вы выбрали: ${event.target.innerText}</p>`;
    });
});
