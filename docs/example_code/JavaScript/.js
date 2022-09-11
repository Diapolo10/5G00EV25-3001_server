"use strict";

// Fetches and prints out the root response

const url = `/`

const getResponse = async url => {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(
            `An error has occurred; $(response.status)`
        );
    }

    const result = await response.json();
    return result;
}

const data = getResponse(url).catch(error => error.message);
console.log(data);
