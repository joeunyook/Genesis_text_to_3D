## Genesis Text-to-3D Backend (FastAPI)

This is the backend for *Genesis: TripoMemories*, a GenAI hackathon project that converts a text prompt or uploaded PNG image into a 3D `.obj` file.

**Live demo (when active):**  
[http://34.16.210.20:8000/docs](http://34.16.210.20:8000/docs) – Swagger UI for prompt/image to 3D generation  
Note: This link only works when the GCP VM is running. Contact the project maintainer to activate it.

## How it works

- **Vertex AI Imagen**: generates a 2D image from a text prompt.
- **TripoSR (open-source)**: converts the image into a `.obj` mesh.
- **FastAPI**: exposes the backend API endpoints.
- **GCP VM + Uvicorn + Firewall**: the app runs on a VM, served by Uvicorn, and is publicly accessible through port 8000.

## Available endpoints

- `POST /generate-obj`: input a text prompt, get an `.obj` file.
- `POST /upload-image`: upload a PNG, get an `.obj` file.

## Notes

This repo does not include the frontend. The backend only runs when the GCP VM is active.

## Credits

TripoSR is an open-source model developed by [VAST-AI-Research/TripoSR](https://github.com/VAST-AI-Research/TripoSR). We use it directly without modification.

@article{TripoSR2024,
  title={TripoSR: Fast 3D Object Reconstruction from a Single Image},
  author={Tochilkin, Dmitry and Pankratz, David and Liu, Zexiang and Huang, Zixuan and and Letts, Adam and Li, Yangguang and Liang, Ding and Laforte, Christian and Jampani, Varun and Cao, Yan-Pei},
  journal={arXiv preprint arXiv:2403.02151},
  year={2024}
}
