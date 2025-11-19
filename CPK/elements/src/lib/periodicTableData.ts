export interface Element {
  atomicNumber: number;
  symbol: string;
  name: string;
  atomicMass: number;
  category: string;
  categoryColor: string;
  period: number;
  group: number;
  electronegativity?: number;
  ionizationEnergy?: number;
  atomicRadius?: number;
  density?: number;
  meltingPoint?: number;
  boilingPoint?: number;
  yearDiscovered?: number;
  state?: string;
}

const COLORS = {
  'Nonmetal': '#90EE90',
  'Reactive Nonmetal': '#FFFF99',
  'Noble Gas': '#FFB6C1',
  'Alkali Metal': '#FFB347',
  'Alkaline Earth Metal': '#FFDAB9',
  'Metalloid': '#D3D3D3',
  'Transition Metal': '#87CEEB',
  'Lanthanide': '#DDA0DD',
  'Actinide': '#F0E68C',
  'Post-transition Metal': '#C0C0C0',
  'Halogen': '#FFCCFF',
};

export const PERIODIC_TABLE: Element[] = [
  // Period 1
  { atomicNumber: 1, symbol: 'H', name: 'Hydrogen', atomicMass: 1.008, category: 'Nonmetal', categoryColor: COLORS['Nonmetal'], period: 1, group: 1, electronegativity: 2.1, ionizationEnergy: 13.6, atomicRadius: 37, density: 0.08988, meltingPoint: -259.16, boilingPoint: -252.87, yearDiscovered: 1766, state: 'Gas' },
  { atomicNumber: 2, symbol: 'He', name: 'Helium', atomicMass: 4.003, category: 'Noble Gas', categoryColor: COLORS['Noble Gas'], period: 1, group: 18, electronegativity: 0, ionizationEnergy: 24.6, atomicRadius: 32, density: 0.1785, meltingPoint: -272.2, boilingPoint: -268.93, yearDiscovered: 1868, state: 'Gas' },

  // Period 2
  { atomicNumber: 3, symbol: 'Li', name: 'Lithium', atomicMass: 6.941, category: 'Alkali Metal', categoryColor: COLORS['Alkali Metal'], period: 2, group: 1, electronegativity: 0.98, ionizationEnergy: 5.39, atomicRadius: 152, density: 0.534, meltingPoint: 180.54, boilingPoint: 1342, yearDiscovered: 1817, state: 'Solid' },
  { atomicNumber: 4, symbol: 'Be', name: 'Beryllium', atomicMass: 9.012, category: 'Alkaline Earth Metal', categoryColor: COLORS['Alkaline Earth Metal'], period: 2, group: 2, electronegativity: 1.57, ionizationEnergy: 9.32, atomicRadius: 112, density: 1.85, meltingPoint: 1287, boilingPoint: 2471, yearDiscovered: 1798, state: 'Solid' },
  { atomicNumber: 5, symbol: 'B', name: 'Boron', atomicMass: 10.811, category: 'Metalloid', categoryColor: COLORS['Metalloid'], period: 2, group: 13, electronegativity: 2.04, ionizationEnergy: 8.30, atomicRadius: 87, density: 2.34, meltingPoint: 2349, boilingPoint: 4200, yearDiscovered: 1808, state: 'Solid' },
  { atomicNumber: 6, symbol: 'C', name: 'Carbon', atomicMass: 12.011, category: 'Nonmetal', categoryColor: COLORS['Nonmetal'], period: 2, group: 14, electronegativity: 2.55, ionizationEnergy: 11.26, atomicRadius: 77, density: 2.26, meltingPoint: 3823, boilingPoint: 4098, yearDiscovered: -1, state: 'Solid' },
  { atomicNumber: 7, symbol: 'N', name: 'Nitrogen', atomicMass: 14.007, category: 'Nonmetal', categoryColor: COLORS['Nonmetal'], period: 2, group: 15, electronegativity: 3.04, ionizationEnergy: 14.53, atomicRadius: 71, density: 1.251, meltingPoint: -210.1, boilingPoint: -195.8, yearDiscovered: 1772, state: 'Gas' },
  { atomicNumber: 8, symbol: 'O', name: 'Oxygen', atomicMass: 15.999, category: 'Nonmetal', categoryColor: COLORS['Nonmetal'], period: 2, group: 16, electronegativity: 3.44, ionizationEnergy: 13.61, atomicRadius: 66, density: 1.429, meltingPoint: -218.79, boilingPoint: -182.95, yearDiscovered: 1774, state: 'Gas' },
  { atomicNumber: 9, symbol: 'F', name: 'Fluorine', atomicMass: 18.998, category: 'Halogen', categoryColor: COLORS['Halogen'], period: 2, group: 17, electronegativity: 3.98, ionizationEnergy: 17.42, atomicRadius: 64, density: 1.696, meltingPoint: -219.62, boilingPoint: -188.12, yearDiscovered: 1886, state: 'Gas' },
  { atomicNumber: 10, symbol: 'Ne', name: 'Neon', atomicMass: 20.180, category: 'Noble Gas', categoryColor: COLORS['Noble Gas'], period: 2, group: 18, electronegativity: 0, ionizationEnergy: 21.56, atomicRadius: 58, density: 0.9002, meltingPoint: -248.59, boilingPoint: -246.05, yearDiscovered: 1898, state: 'Gas' },

  // Period 3
  { atomicNumber: 11, symbol: 'Na', name: 'Sodium', atomicMass: 22.990, category: 'Alkali Metal', categoryColor: COLORS['Alkali Metal'], period: 3, group: 1, electronegativity: 0.93, ionizationEnergy: 5.14, atomicRadius: 186, density: 0.968, meltingPoint: 97.72, boilingPoint: 883, yearDiscovered: 1807, state: 'Solid' },
  { atomicNumber: 12, symbol: 'Mg', name: 'Magnesium', atomicMass: 24.305, category: 'Alkaline Earth Metal', categoryColor: COLORS['Alkaline Earth Metal'], period: 3, group: 2, electronegativity: 1.31, ionizationEnergy: 7.65, atomicRadius: 160, density: 1.738, meltingPoint: 650, boilingPoint: 1091, yearDiscovered: 1755, state: 'Solid' },
  { atomicNumber: 13, symbol: 'Al', name: 'Aluminum', atomicMass: 26.982, category: 'Post-transition Metal', categoryColor: COLORS['Post-transition Metal'], period: 3, group: 13, electronegativity: 1.61, ionizationEnergy: 6.82, atomicRadius: 143, density: 2.70, meltingPoint: 660.32, boilingPoint: 2519, yearDiscovered: 1825, state: 'Solid' },
  { atomicNumber: 14, symbol: 'Si', name: 'Silicon', atomicMass: 28.086, category: 'Metalloid', categoryColor: COLORS['Metalloid'], period: 3, group: 14, electronegativity: 1.90, ionizationEnergy: 8.15, atomicRadius: 117, density: 2.329, meltingPoint: 1414, boilingPoint: 3265, yearDiscovered: 1824, state: 'Solid' },
  { atomicNumber: 15, symbol: 'P', name: 'Phosphorus', atomicMass: 30.974, category: 'Nonmetal', categoryColor: COLORS['Nonmetal'], period: 3, group: 15, electronegativity: 2.19, ionizationEnergy: 10.49, atomicRadius: 107, density: 1.823, meltingPoint: 44.15, boilingPoint: 280.5, yearDiscovered: 1669, state: 'Solid' },
  { atomicNumber: 16, symbol: 'S', name: 'Sulfur', atomicMass: 32.065, category: 'Nonmetal', categoryColor: COLORS['Nonmetal'], period: 3, group: 16, electronegativity: 2.58, ionizationEnergy: 10.36, atomicRadius: 105, density: 2.07, meltingPoint: 115.21, boilingPoint: 444.72, yearDiscovered: -1, state: 'Solid' },
  { atomicNumber: 17, symbol: 'Cl', name: 'Chlorine', atomicMass: 35.453, category: 'Halogen', categoryColor: COLORS['Halogen'], period: 3, group: 17, electronegativity: 3.16, ionizationEnergy: 12.97, atomicRadius: 102, density: 3.214, meltingPoint: -101.5, boilingPoint: -34.04, yearDiscovered: 1774, state: 'Gas' },
  { atomicNumber: 18, symbol: 'Ar', name: 'Argon', atomicMass: 39.948, category: 'Noble Gas', categoryColor: COLORS['Noble Gas'], period: 3, group: 18, electronegativity: 0, ionizationEnergy: 15.76, atomicRadius: 88, density: 1.784, meltingPoint: -189.34, boilingPoint: -185.85, yearDiscovered: 1894, state: 'Gas' },

  // Period 4 - transition metals included
  { atomicNumber: 19, symbol: 'K', name: 'Potassium', atomicMass: 39.098, category: 'Alkali Metal', categoryColor: COLORS['Alkali Metal'], period: 4, group: 1, electronegativity: 0.82, ionizationEnergy: 4.34, atomicRadius: 227, density: 0.862, meltingPoint: 63.38, boilingPoint: 759, yearDiscovered: 1807, state: 'Solid' },
  { atomicNumber: 20, symbol: 'Ca', name: 'Calcium', atomicMass: 40.078, category: 'Alkaline Earth Metal', categoryColor: COLORS['Alkaline Earth Metal'], period: 4, group: 2, electronegativity: 1.00, ionizationEnergy: 6.11, atomicRadius: 197, density: 1.54, meltingPoint: 842, boilingPoint: 1484, yearDiscovered: 1808, state: 'Solid' },
  { atomicNumber: 21, symbol: 'Sc', name: 'Scandium', atomicMass: 44.956, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 3, electronegativity: 1.36, ionizationEnergy: 6.56, atomicRadius: 162, density: 2.985, meltingPoint: 1814, boilingPoint: 3109, yearDiscovered: 1879, state: 'Solid' },
  { atomicNumber: 22, symbol: 'Ti', name: 'Titanium', atomicMass: 47.867, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 4, electronegativity: 1.54, ionizationEnergy: 6.82, atomicRadius: 147, density: 4.506, meltingPoint: 1668, boilingPoint: 3287, yearDiscovered: 1791, state: 'Solid' },
  { atomicNumber: 23, symbol: 'V', name: 'Vanadium', atomicMass: 50.942, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 5, electronegativity: 1.63, ionizationEnergy: 6.74, atomicRadius: 134, density: 6.11, meltingPoint: 1910, boilingPoint: 3407, yearDiscovered: 1801, state: 'Solid' },
  { atomicNumber: 24, symbol: 'Cr', name: 'Chromium', atomicMass: 51.996, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 6, electronegativity: 1.66, ionizationEnergy: 6.77, atomicRadius: 128, density: 7.19, meltingPoint: 1907, boilingPoint: 2671, yearDiscovered: 1797, state: 'Solid' },
  { atomicNumber: 25, symbol: 'Mn', name: 'Manganese', atomicMass: 54.938, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 7, electronegativity: 1.55, ionizationEnergy: 7.43, atomicRadius: 127, density: 7.43, meltingPoint: 1246, boilingPoint: 2061, yearDiscovered: 1774, state: 'Solid' },
  { atomicNumber: 26, symbol: 'Fe', name: 'Iron', atomicMass: 55.845, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 8, electronegativity: 1.83, ionizationEnergy: 7.90, atomicRadius: 124, density: 7.874, meltingPoint: 1538, boilingPoint: 2862, yearDiscovered: -1, state: 'Solid' },
  { atomicNumber: 27, symbol: 'Co', name: 'Cobalt', atomicMass: 58.933, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 9, electronegativity: 1.88, ionizationEnergy: 7.88, atomicRadius: 122, density: 8.9, meltingPoint: 1495, boilingPoint: 2927, yearDiscovered: 1735, state: 'Solid' },
  { atomicNumber: 28, symbol: 'Ni', name: 'Nickel', atomicMass: 58.693, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 10, electronegativity: 1.91, ionizationEnergy: 7.64, atomicRadius: 124, density: 8.908, meltingPoint: 1455, boilingPoint: 2913, yearDiscovered: 1751, state: 'Solid' },
  { atomicNumber: 29, symbol: 'Cu', name: 'Copper', atomicMass: 63.546, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 11, electronegativity: 1.90, ionizationEnergy: 7.73, atomicRadius: 132, density: 8.96, meltingPoint: 1084.62, boilingPoint: 2562, yearDiscovered: -1, state: 'Solid' },
  { atomicNumber: 30, symbol: 'Zn', name: 'Zinc', atomicMass: 65.380, category: 'Transition Metal', categoryColor: COLORS['Transition Metal'], period: 4, group: 12, electronegativity: 1.65, ionizationEnergy: 9.39, atomicRadius: 134, density: 7.134, meltingPoint: 419.53, boilingPoint: 907, yearDiscovered: 1746, state: 'Solid' },
  { atomicNumber: 31, symbol: 'Ga', name: 'Gallium', atomicMass: 69.723, category: 'Post-transition Metal', categoryColor: COLORS['Post-transition Metal'], period: 4, group: 13, electronegativity: 1.81, ionizationEnergy: 5.999, atomicRadius: 141, density: 5.904, meltingPoint: 29.76, boilingPoint: 2204, yearDiscovered: 1875, state: 'Solid' },
  { atomicNumber: 32, symbol: 'Ge', name: 'Germanium', atomicMass: 72.640, category: 'Metalloid', categoryColor: COLORS['Metalloid'], period: 4, group: 14, electronegativity: 2.01, ionizationEnergy: 7.90, atomicRadius: 122, density: 5.323, meltingPoint: 938.25, boilingPoint: 2833, yearDiscovered: 1886, state: 'Solid' },
  { atomicNumber: 33, symbol: 'As', name: 'Arsenic', atomicMass: 74.922, category: 'Metalloid', categoryColor: COLORS['Metalloid'], period: 4, group: 15, electronegativity: 2.18, ionizationEnergy: 9.81, atomicRadius: 119, density: 5.776, meltingPoint: 817, boilingPoint: 614, yearDiscovered: -1, state: 'Solid' },
  { atomicNumber: 34, symbol: 'Se', name: 'Selenium', atomicMass: 78.960, category: 'Nonmetal', categoryColor: COLORS['Nonmetal'], period: 4, group: 16, electronegativity: 2.55, ionizationEnergy: 9.75, atomicRadius: 120, density: 4.809, meltingPoint: 221, boilingPoint: 685, yearDiscovered: 1817, state: 'Solid' },
  { atomicNumber: 35, symbol: 'Br', name: 'Bromine', atomicMass: 79.904, category: 'Halogen', categoryColor: COLORS['Halogen'], period: 4, group: 17, electronegativity: 2.96, ionizationEnergy: 11.81, atomicRadius: 120, density: 3.105, meltingPoint: -7.2, boilingPoint: 58.8, yearDiscovered: 1826, state: 'Liquid' },
  { atomicNumber: 36, symbol: 'Kr', name: 'Krypton', atomicMass: 83.798, category: 'Noble Gas', categoryColor: COLORS['Noble Gas'], period: 4, group: 18, electronegativity: 0, ionizationEnergy: 14.00, atomicRadius: 116, density: 3.749, meltingPoint: -157.36, boilingPoint: -153.22, yearDiscovered: 1898, state: 'Gas' },
];

export const getCategoryColor = (category: string): string => {
  return COLORS[category as keyof typeof COLORS] || '#CCCCCC';
};

export const getElementByAtomicNumber = (atomicNumber: number): Element | undefined => {
  return PERIODIC_TABLE.find(el => el.atomicNumber === atomicNumber);
};

export const getElementsByCategory = (category: string): Element[] => {
  return PERIODIC_TABLE.filter(el => el.category === category);
};

export const getCategories = (): string[] => {
  return Array.from(new Set(PERIODIC_TABLE.map(el => el.category)));
};
