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
    obj = await loadJSON("./help.json");

    now = obj[menu];

    for (const key in now["pages"]){
        if (now["pages"][key]["title"] === submenu){
            now = now["pages"][key];
            break;
        }
    }

    // console.log(obj);
    // console.log(now);

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

    // console.log(text);

    return text;
}

async function initialization(){
    const content = document.querySelector(".content");

    const submenu = document.getElementById("Game Engine 3");
    const menu = submenu.parentElement;

    const text = await loadHelpMenu(menu.id, submenu.id);

    // console.log(text);

    content.innerHTML = text;
}


document.querySelectorAll(".menu-submenu-item").forEach(item => {
    item.addEventListener("click", async event => {
        const content = document.querySelector(".content");

        // const submenu = document.getElementById(event.target.innerText);

        const submenu = document.getElementById(event.currentTarget.id);

        // console.log(submenu, event.target.id);

        const menu = submenu.parentElement;

        const text = await loadHelpMenu(menu.id, submenu.id);

        // console.log(text);

        content.innerHTML = text;
    });
});

initialization()
