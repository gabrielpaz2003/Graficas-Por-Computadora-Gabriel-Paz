use minifb::{Key, Window, WindowOptions};
use image::{ImageBuffer, Rgb};

const WIDTH: usize = 800;
const HEIGHT: usize = 600;

fn main() {
    let mut buffer: Vec<u32> = vec![0; WIDTH * HEIGHT];

    let poligonos = vec![
        vec![(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)],
        vec![(321, 335), (288, 286), (339, 251), (374, 302)],
        vec![(377, 249), (411, 197), (436, 249)],
        vec![(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)],
        vec![(682, 175), (708, 120), (735, 148), (739, 170)],
    ];

    for poligono in poligonos {
        rellenarPoligono(&mut buffer, &poligono);
    }

    guardarBmp(&buffer, "output.bmp").expect("Error al guardar .BMP");

    let mut window = Window::new(
        "Laboratorio 1 - Rellenado de polígonos",
        WIDTH,
        HEIGHT,
        WindowOptions::default(),
    ).unwrap_or_else(|e| {
        panic!("{}", e);
    });

    while window.is_open() && !window.is_key_down(Key::Escape) {
        window.update_with_buffer(&buffer, WIDTH, HEIGHT).unwrap();
    }
}

fn dibujar_linea(buffer: &mut [u32], punto_inicio: (usize, usize), punto_fin: (usize, usize)) {
    let (mut x_actual, mut y_actual) = (punto_inicio.0 as isize, punto_inicio.1 as isize);
    let (x_final, y_final) = (punto_fin.0 as isize, punto_fin.1 as isize);
    let delta_x = (x_final - x_actual).abs();
    let delta_y = -(y_final - y_actual).abs();
    let mut error = delta_x + delta_y;
    let paso_x = if x_actual < x_final { 1 } else { -1 };
    let paso_y = if y_actual < y_final { 1 } else { -1 };

    loop {
        if x_actual >= 0 && x_actual < WIDTH as isize && y_actual >= 0 && y_actual < HEIGHT as isize {
            buffer[(y_actual as usize) * WIDTH + (x_actual as usize)] = 0xff_0000; // Color rojo
        }
        if x_actual == x_final && y_actual == y_final { break; }
        let doble_error = 2 * error;
        if doble_error >= delta_y {
            error += delta_y;
            x_actual += paso_x;
        }
        if doble_error <= delta_x {
            error += delta_x;
            y_actual += paso_y;
        }
    }
}

fn rellenarPoligono(buffer: &mut [u32], polygon: &Vec<(usize, usize)>) {
    let min_y = polygon.iter().map(|&(_, y)| y).min().unwrap() as isize;
    let max_y = polygon.iter().map(|&(_, y)| y).max().unwrap() as isize;

    for y in min_y..=max_y {
        let mut intersections = vec![];
        for i in 0..polygon.len() {
            let mut p1 = polygon[i];
            let mut p2 = polygon[(i + 1) % polygon.len()];
            if p1.1 == p2.1 {
                continue;
            }
            if p1.1 > p2.1 {
                std::mem::swap(&mut p1, &mut p2);
            }
            if (p1.1 as isize <= y) && (y < p2.1 as isize) {
                let x = p1.0 as isize + ((y - p1.1 as isize) * (p2.0 as isize - p1.0 as isize)) / (p2.1 as isize - p1.1 as isize);
                intersections.push(x);
            }
        }
        intersections.sort();
        for i in (0..intersections.len()).step_by(2) {
            if i + 1 < intersections.len() {
                let x1 = intersections[i];
                let x2 = intersections[i + 1];
                for x in x1..=x2 {
                    if x >= 0 && x < WIDTH as isize && y >= 0 && y < HEIGHT as isize {
                        buffer[(y as usize) * WIDTH + (x as usize)] = 0xff_0000;
                    }
                }
            }
        }
    }
}

fn guardarBmp(buffer: &[u32], filename: &str) -> Result<(), Box<dyn std::error::Error>> {
    let mut imgbuf = ImageBuffer::new(WIDTH as u32, HEIGHT as u32);

    for (x, y, pixel) in imgbuf.enumerate_pixels_mut() {
        let index = (y as usize) * WIDTH + (x as usize);
        let color = buffer[index];
        let r = ((color >> 16) & 0xff) as u8;
        let g = ((color >> 8) & 0xff) as u8;
        let b = (color & 0xff) as u8;
        *pixel = Rgb([r, g, b]);
    }

    imgbuf.save(filename)?;
    Ok(())
}
