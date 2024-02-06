
//--Selectors --//
const foundButton = document.getElementById("foundButton")
const graficButton = document.getElementById("graficButton");
const downloadButton = document.getElementById("downloadbutton");

// Function for Show the graffic
function showGrafic(event){
  event.preventDefault();
  let graficImageContainer = document.getElementById("grafic_image")
  graficImageContainer.classList.toggle("hidden");
}
//--Actions--//

graficButton.addEventListener("click",showGrafic)

//Create method for send data filtered 
function sendFilters(event,action){
  event.preventDefault();
  filters = filtersHouses();
  console.log(action)
  let urlHouses ="";
  if(action == "excel"){
    urlHouses = 'http://localhost:8000/houses/houses_excel/'
  }else{
    urlHouses = 'http://localhost:8000/houses/houses_csv/';
  }
  
  // Data for download the exel and the csv file
  const requestData = {
    "filters" : filtersHouses()
    }
  // Configuration of call to API
  const config = {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          'X-CSRF-Token': csrftoken2,
      },
  // data send to API
     body: JSON.stringify(requestData)
  };
// Fecth to server
  fetch(urlHouses, config)
     .then(response => response.blob())
     .then(blob => {
      const reader = new FileReader();
       //Create temporal link
       const url = window.URL.createObjectURL(blob);
       //Create element a
       const a = document.createElement('a');
       // assign the url to link
       a.href = url;
      reader.onloadend = function () {
        // To obtain the first bytes of a Blob object
        const bytes = new Uint8Array(reader.result.slice(0, 4));
        // To check if the first bytes of a Blob match the Excel (xlsx) file format
        const isExcel = bytes[0] === 0x50 && bytes[1] === 0x4B && bytes[2] === 0x03 && bytes[3] === 0x04;
        // To check if the first bytes of a Blob match the CSV file format
        const isCSV = String.fromCharCode.apply(null, bytes) === 'sep=';
  
        if (isExcel) {
          a.download ="Houses.xlsx";
          console.log(" Es Exel");
        } else if (isCSV) {
          a.download = 'Houses.csv';
          console.log('Es csvs');
        }else{
          console.log("NO es ninguno ")
        }
      };
     
      // Put the element a in the body
      document.body.appendChild(a);
      // activate the click programmatically
      a.click();
      //remove the element a 
      document.body.removeChild(a);
      // Delete de provisional URL
      window.URL.revokeObjectURL(url);

     })
     .catch(error => console.log("Error in the download file " +  error))
}
//Get the selectors tocken 
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');


//Create the selector of filterhouses
const filtersHouses = () => {

    filterFeatures = {};
    const city = document.getElementById("provincia")
    console.log(city.value)
    const loc = document.getElementById("loc")
    console.log(loc.value)
    let checkboxs = document.querySelectorAll('input[type="checkbox"]:checked')
    checkboxs.forEach( check => {
    filterFeatures[check.id] = true 
   })
    filterFeatures["location_1"] = city.value;
    filterFeatures["location_2"]=loc.value;
    console.log(filterFeatures);
    return filterFeatures;
   }
// Execute the function
filter = filtersHouses()

//Calculate the diference of prices
function getDifferencePrice(lastPrice,CalculatePrice)
{
  let difference = (lastPrice - CalculatePrice).toFixed(2);
  return parseFloat(difference);
}

//Create the table list from houses
function createTable(houses){
  const tbody = document.getElementById("tbody")
  tbody.innerHTML =""
  console.log(tbody)
  if(houses){
  houses.forEach( house => {
    //Create the tr element
    const tr = document.createElement("tr");
    //Crete the td fot Title
      const tdTitle = document.createElement("td");
      tdTitle.textContent = house.title.charAt(0).toUpperCase() + house.title.slice(1);
      tr.appendChild(tdTitle);
    //Create the td forZoneUrl
      const tdZoneUrl = document.createElement("td");
      const link = document.createElement("a");
      link.href =  house.zone_url;
      const img = document.createElement("img");
      img.src = "../../static/images/hogar.png";
      img.classList.add("houseImg");
      link.appendChild(img)
      tdZoneUrl.appendChild(link)   
      tr.appendChild(tdZoneUrl);
      //Create the  td for LastPrice
      const tdLastPrice = document.createElement("td");
      tdLastPrice.textContent = house.last_price;
      tr.appendChild(tdLastPrice);
      //Create the td for CalculatePrice
      const tdCalculatePrice = document.createElement("td");
      tdCalculatePrice.textContent = house.predicted_price;
      tr.appendChild(tdCalculatePrice);
      //Create the td for tdDiference
      const tdDiference = document.createElement("td");
      tdDiference.textContent = getDifferencePrice(house.last_price,house.predicted_price);
      tr.appendChild(tdDiference);
      //Create Image  for Arrow
      const imgElement = document.createElement("img");
      imgElement.classList.add("imgArrow");
      if (getDifferencePrice(house.last_price,house.predicted_price) >= 0){
        imgElement.src = "../../static/images/flecha-arriba.png";
      }else{
        imgElement.src = "../../static/images/flecha-hacia-abajo.png";
      }
      
      //Create the ed for tdResult
      const tdResult = document.createElement("td");
      tdResult.classList.add("td_arrow")
      tdResult.appendChild(imgElement);
      tr.appendChild(tdResult);
      // Add the file to Table
      tbody.appendChild(tr);
  })
}
}

//Pagination
// Get the selectors
let total_p_button = document.getElementById("numberPages");
let firs_page_a = document.getElementById("first_page_a")
let previous_page_a = document.getElementById("previous_page_a")
let next_page_a = document.getElementById("next_page_a")
let last_page_a = document.getElementById("last_page_a")

// Actual pages data for default
let total_pages = 0;
let actual_page = 1;
// Set the actual Page
function setActualPage(page){
 actual_page = page;
}
//Set the total pages
function SetTotalPage(pages){
  total_pages = pages;
}

//Received the actual page and call Method fef
function count_pages(option){
 
  let request_page = 0;
  switch(option){
    case "next":
      request_page = actual_page + 1;
      break;
    case "previous":
      request_page = actual_page - 1;
      console.log("Pagina desde previous" + request_page)
      break;
    case "last":
      request_page = total_pages;
      setActualPage(total_pages);
      break;
    default:
      request_page = 1
      break;
  }
  console.log("Recibido en el Count_pages"  + actual_page)
  fet(request_page);
  
}

// Function for paginate the houses in the view 
let option = "";
last_page_a.addEventListener("click", (event) => {
  console.log("Pinchado last button y mandado pagina" + total_pages)
  event.preventDefault();
  option = "last";
  count_pages(option);
})

// --LISTENER OF PAGINATION BUTTONS --//

firs_page_a.addEventListener("click", (event) => {
  event.preventDefault();
  count_pages(1);
})

previous_page_a.addEventListener("click", (event) => {
  event.preventDefault();
  option = "previous";
  count_pages(option);
})

next_page_a.addEventListener("click", (event) => {
  event.preventDefault();
  option = "next";
  count_pages(option);
})

// Function for received the list of houses
const csrftoken2 = document.querySelector('[name=csrfmiddlewaretoken]').value;
//Function for call backend and get the list of houses
    const fet = (actual_page) => {
      //Check if the actual page received is not null
      if (actual_page == null){
        actual_page = "1"
      }else{
        actual_page = actual_page
      }

      console.log("Numero de pagina enviada a la API" + actual_page)
      // Url of API 
      const urlHouses = 'http://localhost:8000/houses/houses/';
      // Data for send to API
      const requestData = {
        "page":actual_page,
        "filters" : filtersHouses()
        }
      // Configuration of call to API
      const config = {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              'X-CSRF-Token': csrftoken2,
          },
      // data send to API
         body: JSON.stringify(requestData)
      };
      // Fetch to API
      fetch(urlHouses, config)
          .then(response => {
              if (!response.ok) {
                 throw new Error(`Network response was not ok. Status: ${response.status}`);
              }
              return response.json();
          })
           .then(data => {
            // List of Houses
              houses = data.houses
            // Create the table
              createTable(houses)
            //Number of pages receives from the API
              total_pages = data.pages
            //Page actual received from the API
              SetTotalPage(total_pages)
              actual_page = data.actual_page;
              setActualPage(actual_page);
              //Set the text for the total_button
              total_p_button.textContent = ` de ${total_pages}`;
              console.log("Este es el numero de pagina actual recibida desde la Api " +data.actual_page)
            // Paginate the list in front view
            console.log("Numero de Paginas Totales" + total_pages)
            console.log(actual_page)
             // pagination(total_pages,actual_page)
             if(actual_page == total_pages){
              next_page_a.classList.add("oculto");
            }else{
              next_page_a.classList.remove("oculto")    
            }

            let spanPreviousPage= document.getElementById("spanPreviousPage");
            if (actual_page == 1){
              previous_page_a.classList.add("oculto");
              spanPreviousPage.classList.add("oculto");
            }else{
              previous_page_a.classList.remove("oculto");
              spanPreviousPage.classList.remove("oculto");
            }

            firs_page_a.textContent=actual_page
            
           })
          .catch(error => {
              console.error('Fetch error:', error);
          });
    };
// launch list of all the houses with the filters
foundButton.addEventListener("click",(event)=>{
  event.preventDefault()
  const trTable = document.getElementById("trTable");
  trTable.innerHTML = "";
  const headers = ["Casa","Link","Precio Vivienda","Precio Calculado"
                  ,"Diferencia","Resultado"];

  headers.forEach(value => {
    const thHeader = document.createElement("th");
    thHeader.innerHTML = value;
    trTable.appendChild(thHeader);
  })



// --- Download files ---//
  const downloadButton = document.createElement("button")
  downloadButton.id = "downloaCsv";
  downloadButton.addEventListener("click",sendFilters);
  const imagen = document.createElement("img");
  imagen.classList.add("imgDownload");
  imagen.src = "../../static/images/csv.png";  
  imagen.alt = "Descripción de la imagen";  
  downloadButton.appendChild(imagen);
  let nuevaCelda = document.createElement("th");
  nuevaCelda.id = "nuevaCelda";
  nuevaCelda.appendChild(downloadButton);
  let primeraFila = document.querySelector("thead tr");
  primeraFila.appendChild(nuevaCelda);
  // Second button to download exel
  const downloadExcel = document.createElement("button");
  downloadExcel.id = "downloadExcel";
  let action = "excel";
  downloadExcel.addEventListener("click", (event) => sendFilters(event,action));

  const imageExcel = document.createElement("img");
  imageExcel.classList.add("imgDownload");
  imageExcel.src = "../../static/images/exel.png";  // Reemplaza con la ruta de tu imagen
  imageExcel.alt = "Descripción de la imagen";  // Reemplaza con la descripción de tu imagen
  downloadExcel.appendChild(imageExcel);
  let newCell = document.createElement("th");
  newCell.appendChild(downloadExcel);  // Aquí corregí downloadButton por downloadExel
  primeraFila.appendChild(newCell);
  fet();
})

// -- CHECKBOXES HOUSES TYPE --//

//Selection of checkboxes of House type
const checkboxTypes = document.querySelectorAll('.checkboxType')
// Function for only select one Type
checkboxTypes.forEach((check => {
  check.addEventListener('click', () => {
    checkboxTypes.forEach((otherCheck)=>{
      if(otherCheck !== check){
        otherCheck.checked = false;
      }
    })
  })
}))




