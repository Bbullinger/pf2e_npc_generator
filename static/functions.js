const BASE_URL = "http://localhost:5000/";

function selectFormElement(element) {
  return document.querySelector(element);
}

//Pick a random based on given max, rounded down to whole number ( range is 0 - max)
function randomNumber(max) {
  return Math.floor(Math.random() * max + 1);
}

//contact python server to use API KEY, then contact python to return a random element
//of endpoint in json format
async function randomAPI(endpoint) {
  const response = await axios.get(`${BASE_URL}/${endpoint}`);
  //Grab num of results, find a random number from 1 - numResults, and return endpoint result
  //index of the random number in string format
  const numResults = response.data.results.length;
  return response.data.results[randomNumber(numResults)].name;
  // const numResults = response.length;
  // return response[randomNumber(numResults)].name;
}
async function endpointAPI(endpoint) {
  const response = await axios.get(`${BASE_URL}/${endpoint}`);
  console.log(response);
  return response.data.results;
}

//This function pulls data from the pf2e api as well as offers random numbers for stats (from 8-14)

async function randomizeNpcForm() {
  // Spells and Name excluded in form auto fill, as they are optional
  const formAPIValues = [
    generatorBackground,
    generatorAncestry,
    generatorClass,
    // generatorAncestryFeats,
    // generatorClassFeats,
  ];
  for (let formInput of formAPIValues) {
    //Form is created using wtf-forms in a python file. Some python variable naming
    //conventions conflict with API endpoints names, these if statements are a work around
    if (formInput === generatorClass) {
      formInput.value = await randomAPI("class");
      // } else if (formInput === generatorAncestryFeats) {
      //   formInput.value = await randomAPI("ancestryFeature");
      // } else if (formInput === generatorClassFeats) {
      //   formInput.value = await randomAPI("classFeature");
    } else {
      formInput.value = await randomAPI(formInput.name);
    }
  }

  //Stats seperated from API values as they do not need an API call to fill
  const formStatsValues = [
    generatorStr,
    generatorCon,
    generatorWis,
    generatorDex,
    generatorInt,
    generatorCha,
  ];
  for (let formInput of formStatsValues) {
    //Want the values to be between 8 and 16. Base set at 8, function adds 0 to 6
    formInput.value = randomNumber(6) + 10;
  }
  generatorLevel.value = randomNumber(20);
}

function createCharLink(character) {
  const span = document.createElement("span");
  span.setAttribute("class", "char-link");
}

async function getTableDB(apiRoute) {
  const response = await axios.get(`${BASE_URL}${apiRoute}`);
  return response.data;
}

async function getDB(tableName) {
  const tableData = await getTableDB(`/get_${tableName}`);
  return tableData;
}
function displayChar(characterObj) {
  displayName.innerText = characterObj.name;
  displayBackground.innerText = characterObj.background;
  displayAncestry.innerText = characterObj.ancestry;
  displayClass.innerText = characterObj.char_class;

  displayLevel.innerText = characterObj.level;

  displayStr.innerText = characterObj.strength;
  displayCon.innerText = characterObj.con;
  displayWis.innerText = characterObj.wis;
  displayDex.innerText = characterObj.dex;
  displayInt.innerText = characterObj.intel;
  displayCha.innerText = characterObj.cha;
}

//Grabs all groups created by user, which were stored in DB, and displays under group form.
async function displayGroups() {
  const groups = await getDB("groups");

  for (let group of groups) {
    //Create an li element to display each group, and add to group name list
    const newLi = document.createElement("li");
    newLi.setAttribute("class", "group-name");
    newLi.dataset.name = group.group_name;
    newLi.innerText = group.group_name;
    groupName.append(newLi);

    //add a second list to group, used to display characters of that group
    const newUl = document.createElement("ul");
    newUl.setAttribute("class", "character-list");
    newUl.setAttribute("id", `${group.group_name}-characters`);
    newLi.append(newUl);

    //Add another li to be used to add characters to this group
    const addForm = document.createElement("form");
    newUl.append(addForm);
    newLi.setAttribute("class", "group-add-character");
    newLi.setAttribute("id", `${group.group_name}-add-character`);
    newLi.innerText = "Click to add character";
    newUl.append(newLi);
  }
}
