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
    //Want the values to be between 8 and 14. Base set at 8, function adds 0 to 6
    formInput.value = randomNumber(6) + 8;
  }
  generatorLevel.value = randomNumber(20);
}
