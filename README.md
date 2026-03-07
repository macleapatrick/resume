# Resume

PDF resume generator and local web viewer.

## Setup

```bash
git clone https://github.com/macleapatrick/resume.git
cd resume
pip install flask reportlab
```

## Usage

### Web viewer

```bash
python app.py
```

Open [http://localhost:5050](http://localhost:5050) to view the resume in your browser. Click **Download PDF** to export.

### Generate PDF directly

```bash
python resume_generator.py
```

Outputs `patrick_maclea_resume.pdf` to the configured path.
