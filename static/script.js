const urlBase = "http://127.0.0.1:5000/api";

function displayCupcake(cupcake) {
    cupcakeHTML = `
    <div id=${cupcake.id}>
        <img src="${cupcake.image}" alt="There is no image for this cupcake">
        <li>
            <p>flavor: ${cupcake.flavor}</p>
            <p>size: ${cupcake.size}</p>
            <p>rating: ${cupcake.rating}</p>
            <button class="delete">Delete Cupcake</button>
        </li>
    </div>
    `;
    $("#cupcake_list").append(cupcakeHTML);
}

async function displayInitialCupcakes() {
    const JSONResponse = await axios.get(urlBase + "/cupcakes");
    cupcakes = JSONResponse.data.cupcakes;
    
    for (let cupcake of cupcakes) {
        displayCupcake(cupcake);
    }
}

$("#add_cupcake").on("submit", async function (e) {
    e.preventDefault();

    const flavor = $("#form_flavor").val();
    const size = $("#form_size").val();
    const rating = $("#form_rating").val();
    const image = $("#form_image").val();
    const url = urlBase + "/cupcakes"

    const addCupcakeJSON = await axios.post(url, {
        flavor,
        size,
        rating,
        image
    });

    cupcake = addCupcakeJSON.data.cupcake;
    displayCupcake(cupcake);

    $("add_cupcake").trigger("reset");
});

$("#cupcake_list").on("click", ".delete", async function (e) {
    e.preventDefault();

    const id = $(e.target).closest("div").attr("id");

    //remove cupcake from the database and html page
    url = urlBase + "/cupcakes/" + id;
    await axios.delete(url);
    $(e.target).closest("div").remove();
});

$(displayInitialCupcakes);