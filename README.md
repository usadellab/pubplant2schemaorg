# PubPlant Genome Metadata Transformer

This repository automates the transformation of genomic metadata from **PubPlant** into **Schema.org/Dataset** JSON-LD. This initiative supports the **FAIRagro middleware**, contributing to a federated Research Data Infrastructure (RDI) for agrosystems science.

By standardizing this data, we enable seamless integration with the **FAIRagro search portal** and **Scientific Workflow infrastructures (SciWin)**.

---

## 🧬 Purpose & Context

**PubPlant** (https://www.plabipd.de/pubplant_main.html) is a continuously updated online resource that tracks published plant genome sequences. It focuses on the **Archaeplastida** group, ensuring that included genomes are comprehensively described with assembly, scaffolding, and structural gene annotation.

As the pace of plant genome sequencing accelerates—surpassing 1,800 species by late 2024 —this repository ensures that these metadata records are:
* **Findable**: Discoverable via federated search portals.
* **Interoperable**: Mapped to the global Schema.org standard.
* **Reusable**: Provided with clear licensing and citation metadata.

---

## 🛠️ Technical Architecture

The repository functions as a "serverless" ETL (Extract, Transform, Load) pipeline that generates a static API hosted on GitHub Pages.

### 1. Extraction (`build_static.py`)
The pipeline fetches the latest curated records from the PubPlant source (`genomes_timeline1.json`).

### 2. Transformation (`schema_transformer.py`)
The transformation logic converts internal database structures into a **Schema.org/Dataset** profile:
* **Authorship**: Parses complex strings (e.g., "Yu J, Hu S") into structured `Person` or `Organization` entities. **Note**: Only the first two authors of a publication are retrieved. 
* **Identification**: Maps Publication DOIs to the `@id` and `identifier` fields for persistent referencing.
* **Descriptions**: Automatically generates human-readable summaries including scientific names, common names, and genome sizes in Mb.
* **Categorization**: Utilizes taxonomic classifications (Angiosperms, Gymnosperms, Algae, etc.) as keywords.

### 3. Loading & Deployment (`deploy.yml`)
The project is deployed via **GitHub Actions**:
* **Automation**: Runs every day at 00:00 UTC to sync with PubPlant updates.
* **Hosting**: The transformed JSON is published to the `gh-pages` branch, making it accessible as a static endpoint for the FAIRagro middleware.

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `build_static.py` | Main execution script for fetching and saving data. |
| `schema_transformer.py` | Mapping logic for Schema.org conversion. |
| `deploy.yml` | GitHub Actions workflow for CI/CD. |
| `public/genomes.json` | The final transformed FAIR-compliant metadata file. |

---

## 🎓 Citation & Attribution

Data source provided by **Forschungszentrum Jülich GmbH, IBG-4 Bioinformatics**.

If you use this data in your research, please cite the original PubPlant publication:
> Schwacke R, Bolger ME and Usadel B (2025) PubPlanta continuously updated online resource for sequenced and published plant genomes. Front. Plant Sci. [cite_start]16:1603547. doi: 10.3389/fpls.2025.1603547.

---
*Developed as part of the FAIRagro federated RDI initiative.*
