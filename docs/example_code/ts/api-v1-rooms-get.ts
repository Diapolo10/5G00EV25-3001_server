/**
 * Fetch a list of public rooms from the API
 */

import fetch from 'node-fetch';

type Room = {
  id: number;
  name: string;
  public: boolean;
  owner: string | null;
};

type GetRoomsResponse = {
  data: Room[];
};

async function getRooms() {
  try {
    const response = await fetch('localhost:11037/api/v1/rooms', {
      method: 'GET',
      headers: {
        Accept: 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Error! status: ${response.status}`);
    }

    const result = (await response.json()) as GetRoomsResponse;

    console.log('result is: ', JSON.stringify(result, null, 4));

    return result;
  } catch (error) {
    if (error instanceof Error) {
      console.log('error message: ', error.message);
      return error.message;
    } else {
      console.log('unexpected error: ', error);
      return 'An unexpected error occurred';
    }
  }
}

getRooms();
