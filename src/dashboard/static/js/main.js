/* const { fill } = require("core-js/core/array")
const { data } = require("jquery") */

const a1 = document.querySelector("#view-snap1")
const a2 = document.querySelector("#view-snap2")

var $filterBy = $(".filter-icon")
var $exit = $(".exit-icon")
var $filtrarForm = $(".form-filter")
var $filtrarButton = $(".form-submit button")

const grafico = document.querySelector("#grafico")
const wordcloud = document.querySelector("#wordcloud")
const filter = document.querySelector("#filter-by-icon")
const temp_div = document.querySelector("#filter-by")

document.body.style.zoom = "1.08"



console.log(`grafico = ${$("#grafico iframe").attr("name")} `)

/* if ($("#grafico iframe").attr("name") == "custom") {
    // Realiza a chamada para fazer o grafico
    const pisDataset = $("#charts-parameters").children().eq(0)
    const wordcloudDataset = $("#charts-parameters").children().eq(1)
    var instituicoes = $("#charts-parameters").children().eq(2).text()
    instituicoes = instituicoes.replace(/'/g, '"')
    console.log(`pisDataset = ${pisDataset.text()}, \n wordcloudDataset = ${wordcloudDataset.text() }, \n instituicoes = ${instituicoes}`);
    makingCharts(wordcloudDataset.text(), pisDataset.text(), instituicoes)
}
 */

a1.addEventListener("click", (event) => {
    event.preventDefault()
    grafico.scrollIntoView({ behavior: "smooth", block: "end" })
})

a2.addEventListener("click", (event) => {
    event.preventDefault()
    wordcloud.scrollIntoView({ behavior: "smooth", block: "end" })
})

$exit.on("click", () => {
    $("#filter-by").css("display", "none")
})

$filterBy.on("click", () => {
    $("#filter-by").css("display", "flex")
})

function fill_charts(html_src, png_src) {
    /* a */
    $("#grafico p").remove()
    $("#wordcloud p").remove()
    $("#grafico iframe").attr("src", html_src).css("visibility", "visible")
    $("#wordcloud img").attr("src", png_src).css("visibility", "visible")

    if (!html_src || !png_src) {

        if (!html_src) {
            $("#grafico iframe").css("visibility", "hidden")
            $("#grafico").prepend(
                `<p class="center-text" style="margin-top:25%">Nao foi possivel gerar o grafico das PIs aos anos</p>`
            )
        }
        if (!png_src) {
            $("#wordcloud img").css("visibility", "hidden")
            $("#wordcloud").prepend(
                `<p class="center-text" style="margin-top:25%">Nao foi possivel gerar a Wordcloud</p>`
            )
        }
        return
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function makingCharts(wordcloud_dataset, pis_dataset, instituicoes) {
    // Faz a chamada pra o backend gerar os graficos a partir dos datasets e instituicoes providas
    console.log(`"Making Chart" with wordcloud_dataset = ${wordcloud_dataset}, pis_dataset = ${pis_dataset}, instituicoes = ${instituicoes}`);
    $.ajax({
        method: $("#parameters").attr("method"),
        url: $("#parameters").attr("urlPisChart"),
        data: {
            wordcloud_dataset: wordcloud_dataset,
            pis_dataset: pis_dataset,
            instituicoes: instituicoes,
        },
        success: function (data) {
            console.log(`arquivos gerados ${data}`)
            console.log(data)
            fill_charts(
                // Nomes dos arquivos gerados
                data["chart_pis_result"],
                data["chart_wordcloud_result"]
            )
        },
        error: function (error) {
            console.log(
                `GOT ERROR during ajax on setting CHARTS, ${JSON.stringify(
                    error
                )}`
            )
        },
    })
}

function sayHi() {
    console.log("Hi")
}

function refresh_data() {
    function get_form_data() {
        var data = {}

        $filtrarForm.serializeArray().forEach((item) => {
            data[item.name] = item.value
        })
        console.log(`data = ${JSON.stringify(data)}`)
        return data
    }

    function fill_pis_count(data) {
        const $pi_terms = $(".text-wrapper-2.center-text")
        console.log($pi_terms)
        console.log(data["patent_count"])
        $($pi_terms[0]).text(data["patent_count"])
        $($pi_terms[1]).text(data["computer_software_count"])
        $($pi_terms[2]).text(data["brand_count"])
        $($pi_terms[3]).text(data["industrial_design_count"])
    }

    function fill_top_titulares(data) {
        const $titulares = $("#titulares .table-layout")
        $titulares.empty()
        if (data.length == 0) {
            $titulares.append(`<tr>
                  <td colspan="3" class="center-text">Nenhum titular encontrado</td>
                </tr>`)
            return
        }
        const firstRowString = `
					<tr>
						<td>
							<span class="special-entity">#1</span>
						</td>
						<td class="entity">${data[0]["pessoa__nome"]}</td>
						<td>${data[0]["qtde_pis_publicadas"]}</td>
					</tr>`
        $titulares.append(firstRowString)
        for (let i = 1; i < data.length && i < 10; i++) {
            const rowString = `
				<tr>
					<td>#${i + 1}</td>
					<td class="entity">${data[i]["pessoa__nome"]}</td>
					<td>${data[i]["qtde_pis_publicadas"]}</td>
				</tr>`
            $titulares.append(rowString)
        }
    }

    function fill_top_inventores(data) {
        const $inventores = $("#inventores .table-layout")
        $inventores.empty()
        if (data.length == 0) {
            $inventores.append(`<tr>
                  <td colspan="3" class="center-text">Nenhum inventor encontrado</td>
                </tr>`)
            return
        }
        const firstRowString = `
				<tr>
					<td><span class="special-entity">#1</span></td>
					<td class="entity">${data[0]["pessoa__nome"]}</td>
					<td>${data[0]["qtde_pis_publicadas"]}</td>
				</tr>
			`
        $inventores.append(firstRowString)
        for (let i = 1; i < data.length && i < 10; i++) {
            const rowString = `
				<tr>
					<td>#${i + 1}</td>
					<td class="entity">${data[i]["pessoa__nome"]}</td>
					<td>${data[i]["qtde_pis_publicadas"]}</td>
				</tr>`
            $inventores.append(rowString)
        }
    }

    form_data = get_form_data()
    const csrftoken = getCookie('csrftoken');

    $filtrarForm.off("submit").on("submit", (event) => {
        event.preventDefault()
        if (Object.keys(form_data).length == 1) {
            alert("Selecione pelo menos uma instituicao")
            return
        }
        if (Object.keys(form_data).length == 2) {
            // console.log("Instituicao selecionada = " + Object.keys(form_data)[1]);
            $("#panel-name").text(Object.keys(form_data)[1])
        }
        else {
            $("#panel-name").text("MULTI-INSTITUIÇÃO")
        }
        $.ajax({
            method: $filtrarForm.attr("method"),
            headers: { "X-CSRFToken": csrftoken },
            url: $filtrarForm.attr("action"),
            data: form_data,
            success: function (data) {
                console.log(data)
                fill_pis_count(data["pis_count"])
                fill_top_titulares(data["top_titulares"])
                fill_top_inventores(data["top_inventors"])
                // Fazendo o grafico agora
                makingCharts(data["wordcloud_dataset"], data["pis_dataset"], data["instituicoes"])
            },
        })
    })
}




$filtrarButton.on("click", () => refresh_data())


//$("#Regiao").geocomplete()




/* Animando a cidade! */
