use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    
    let room_id = "7b039c76-e656-454e-a97a-85e7490bade4";
    let url = format!(
        "/api/v1/rooms/{}",
        &room_id
    );

    let response = reqwest::blocking::get(&url)?.text()?;
    println!("{:#?}", resp);
    Ok(())
}
