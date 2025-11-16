package periodictable

// Element represents a chemical element with its properties
type Element struct {
	ID              int     `json:"id"`
	Symbol          string  `json:"symbol"`
	Name            string  `json:"name"`
	AtomicNumber    int     `json:"atomicNumber"`
	AtomicMass      float64 `json:"atomicMass"`
	Electrons       int     `json:"electrons"`
	Protons         int     `json:"protons"`
	Neutrons        int     `json:"neutrons"`
	Category        string  `json:"category"`
	Color           string  `json:"color"`
	ElectronConfig  string  `json:"electronConfig"`
	Valence         int     `json:"valence"`
	Electronegativity float64 `json:"electronegativity"`
	Description     string  `json:"description"`
	// 3D Model Properties
	VDWRadius       float64 `json:"vdwRadius"`
	CovalentRadius  float64 `json:"covalentRadius"`
}

// ElementDatabase holds all periodic table elements
type ElementDatabase struct {
	Elements map[string]*Element
}

// NewElementDatabase creates and initializes the periodic table database
func NewElementDatabase() *ElementDatabase {
	db := &ElementDatabase{
		Elements: make(map[string]*Element),
	}
	db.initializeElements()
	return db
}

// GetElement returns an element by symbol
func (db *ElementDatabase) GetElement(symbol string) *Element {
	return db.Elements[symbol]
}

// GetElementByAtomicNumber returns an element by atomic number
func (db *ElementDatabase) GetElementByAtomicNumber(atomicNum int) *Element {
	for _, elem := range db.Elements {
		if elem.AtomicNumber == atomicNum {
			return elem
		}
	}
	return nil
}

// GetAllElements returns all elements
func (db *ElementDatabase) GetAllElements() []*Element {
	elements := make([]*Element, 0, len(db.Elements))
	for _, elem := range db.Elements {
		elements = append(elements, elem)
	}
	return elements
}

// initializeElements populates the database with periodic table elements (sample)
func (db *ElementDatabase) initializeElements() {
	elements := []*Element{
		{
			ID:               1,
			Symbol:           "H",
			Name:             "Hydrogen",
			AtomicNumber:     1,
			AtomicMass:       1.008,
			Electrons:        1,
			Protons:          1,
			Neutrons:         0,
			Category:         "nonmetal",
			Color:            "#FFFFFF",
			ElectronConfig:   "1s¹",
			Valence:          1,
			Electronegativity: 2.20,
			Description:      "Lightest element, essential for water and organic molecules",
			VDWRadius:        1.20,
			CovalentRadius:   0.31,
		},
		{
			ID:               2,
			Symbol:           "He",
			Name:             "Helium",
			AtomicNumber:     2,
			AtomicMass:       4.003,
			Electrons:        2,
			Protons:          2,
			Neutrons:         2,
			Category:         "noblegas",
			Color:            "#FFC0CB",
			ElectronConfig:   "1s²",
			Valence:          0,
			Electronegativity: 0.00,
			Description:      "Inert noble gas, second most abundant element in universe",
			VDWRadius:        1.40,
			CovalentRadius:   0.28,
		},
		{
			ID:               6,
			Symbol:           "C",
			Name:             "Carbon",
			AtomicNumber:     6,
			AtomicMass:       12.011,
			Electrons:        6,
			Protons:          6,
			Neutrons:         6,
			Category:         "nonmetal",
			Color:            "#909090",
			ElectronConfig:   "1s² 2s² 2p²",
			Valence:          4,
			Electronegativity: 2.55,
			Description:      "Foundation of organic chemistry, forms diverse compounds",
			VDWRadius:        1.70,
			CovalentRadius:   0.76,
		},
		{
			ID:               8,
			Symbol:           "O",
			Name:             "Oxygen",
			AtomicNumber:     8,
			AtomicMass:       15.999,
			Electrons:        8,
			Protons:          8,
			Neutrons:         8,
			Category:         "nonmetal",
			Color:            "#FF0000",
			ElectronConfig:   "1s² 2s² 2p⁴",
			Valence:          6,
			Electronegativity: 3.44,
			Description:      "Essential for respiration, highly reactive non-metal",
			VDWRadius:        1.52,
			CovalentRadius:   0.66,
		},
		{
			ID:               26,
			Symbol:           "Fe",
			Name:             "Iron",
			AtomicNumber:     26,
			AtomicMass:       55.845,
			Electrons:        26,
			Protons:          26,
			Neutrons:         30,
			Category:         "transitionmetal",
			Color:            "#FFA500",
			ElectronConfig:   "[Ar] 3d⁶ 4s²",
			Valence:          8,
			Electronegativity: 1.83,
			Description:      "Essential transition metal, basis of steel production",
			VDWRadius:        2.04,
			CovalentRadius:   1.32,
		},
		{
			ID:               79,
			Symbol:           "Au",
			Name:             "Gold",
			AtomicNumber:     79,
			AtomicMass:       196.967,
			Electrons:        79,
			Protons:          79,
			Neutrons:         118,
			Category:         "transitionmetal",
			Color:            "#FFD700",
			ElectronConfig:   "[Xe] 4f¹⁴ 5d¹⁰ 6s¹",
			Valence:          1,
			Electronegativity: 2.54,
			Description:      "Precious metal, highly valued for electronics and jewelry",
			VDWRadius:        2.66,
			CovalentRadius:   1.34,
		},
	}

	for _, elem := range elements {
		db.Elements[elem.Symbol] = elem
	}
}
