from fastapi import HTTPException

import base64
import tempfile
import os
import numpy as np
import json
from app.schemas.pdf_request import PDFRequest
from app.extractors.hdfc_extractor import extract_transactions
from app.services.hybrid_pdf_service import (process_hybrid_pdf)


async def extract_table_from_pdf(
    request: PDFRequest
):
    try:

        pdf_bytes = base64.b64decode(
            request.pdf_base64
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_pdf:

            temp_pdf.write(pdf_bytes)
            pdf_path = temp_pdf.name

        table_data, outside_data = (
            process_hybrid_pdf(pdf_path)
        )
        transaction_data = (
            extract_transactions(pdf_path)
        )

        os.remove(pdf_path)

        if not table_data:
            raise HTTPException(
                status_code=404,
                detail="No table found"
            )

        rows = [
            r for r in table_data
            if isinstance(r, list)
        ]

        headers = rows[0]
        data_rows = rows[1:]

        json_data = []

        for row in data_rows:

            obj = {}

            for i, col in enumerate(headers):

                obj[col] = (
                    row[i]
                    if i < len(row)
                    else ""
                )

            json_data.append(obj)

        for r in json_data:

            for k, v in r.items():

                if (
                    v is None
                    or (
                        isinstance(v, float)
                        and np.isnan(v)
                    )
                ):
                    r[k] = ""

        result = {
            "status": "success",
            "file_name": request.file_name,
            "outside_data": outside_data,
            "table_data": json_data,
            "transaction_data": transaction_data
        }

        # ============================
        # SAVE OUTPUT TO JSON FILE
        # ============================
        output_dir = "BOB"
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(
            output_dir,
            f"{request.file_name or 'output'}.json"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )