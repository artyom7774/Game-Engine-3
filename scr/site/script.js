async function loadJSON(filePath) {
    try {
        const response = await fetch(filePath);

        if (!response.ok) {
            throw new Error("Сеть не в порядке: " + response.statusText);
        }

        const data = await response.json();

        return data;

    } catch (error) {
        console.error("Ошибка загрузки JSON:", error);
    }
}


async function loadHelpMenu(menu, submenu){
    help = await loadJSON("./help.json");

    now = help[menu];

    for (const key in now["pages"]){
        if (now["pages"][key]["title"] === submenu){
            now = now["pages"][key];
            break;
        }
    }

    variables = [];

    variables.push(`<p class="big-help-text">\t${now["title"]}</p>`);

    for (const key in now["text"]){
        variables.push(`<p class="help-text">${now["text"][key]}</p>`);
    }

    text = "";

    for (const index in variables){
        text += variables[index];
    }

    text = "<div>" + text + "</div>";

    return text;
};


document.querySelectorAll(".menu-submenu-item").forEach(item => {
    item.addEventListener("click", async event => {
        const content = document.querySelector(".content");

        const submenu = document.getElementById(event.currentTarget.id);
        const menu = submenu.parentElement;

        const text = await loadHelpMenu(menu.id, submenu.id);

        content.innerHTML = text;
    });
});


async function initialization(){
    const contentClass = document.querySelector(".content");
    
    // SET STAT CONTENT TEXT

    const submenu = document.getElementById("Game Engine 3");
    const menu = submenu.parentElement;

    contentClass.innerHTML = await loadHelpMenu(menu.id, submenu.id);
};


initialization();
