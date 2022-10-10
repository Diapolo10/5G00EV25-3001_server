use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {

    let url = "/api/v1/rooms";

    let response = reqwest::blocking::get(&url)?.text()?;
    println!("{:#?}", resp);
    Ok(())
}
