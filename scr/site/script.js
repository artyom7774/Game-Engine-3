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


async function initialization(){        
    // INIT MENU ELEMENTS

    const contentMenu = document.querySelector(".menu");

    help = await loadJSON("./help.json");

    text = "";

    for (const name in help){
        text += `<li class="menu-submenu" id="${help[name]["name"]}">${help[name]["name"]}`;

        index = 0;

        for (const page in help[name]["pages"]){
            text += `<div class="menu-submenu-element">`;

            if (Object.keys(help[name]["pages"]).length - 1 === index){
                text += `<svg height="30" width="26"><polyline points="10,0 10,15 25,15" style="fill:none;stroke:white;stroke-width:1" /></svg>`;
            } else {
                text += `<svg height="30" width="26"><polyline points="10,0 10,15 25,15 10,15 10,30" style="fill:none;stroke:white;stroke-width:1" /></svg>`;
            }

            text += `<p class="menu-submenu-item" id="${help[name]["pages"][page]["title"]}">${help[name]["pages"][page]["title"]}</p>`;
            text += `</div>`;

            index += 1;
        }

        text += `</li>`
    }

    contentMenu.innerHTML = text;

    // SET START CONTENT TEXT

    const contentClass = document.querySelector(".content");

    const submenu = document.getElementById("Game Engine 3");
    const menu = submenu.parentElement.parentElement;

    contentClass.innerHTML = await loadHelpMenu(menu.id, submenu.id);

    // INIT

    addMenuEventListeners();
};


function addMenuEventListeners() {
    document.querySelectorAll(".menu-submenu-item").forEach(item => {
        item.addEventListener("click", async event => {
            const content = document.querySelector(".content");

            const submenu = document.getElementById(event.currentTarget.id);
            const menu = submenu.parentElement.parentElement;

            const text = await loadHelpMenu(menu.id, submenu.id);
            content.innerHTML = text;
        });
    });
};


document.addEventListener('DOMContentLoaded', function () {
    initialization();
});
