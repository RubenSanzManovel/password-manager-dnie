import sys
import os
from cryptography import x509
from pkcs11 import lib as pkcs11_lib, ObjectClass, Attribute

# --- Ruta Fija de la Librería ---
PKCS11_LIB_PATH = r"C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll"

def parse_and_print_certificate(cert_obj, cert_name):
    """
    Función auxiliar para analizar e imprimir un objeto de certificado.
    """
    try:
        print(f"\n--- Certificado Encontrado: {cert_name} ---")
        der_data = cert_obj[Attribute.VALUE]
        cert = x509.load_der_x509_certificate(der_data)

        subject = cert.subject
        issuer = cert.issuer

        print(f"  Propietario (Subject): {subject.rfc4514_string()}")
        print(f"  Emitido por (Issuer): {issuer.rfc4514_string()}")
        print(f"  Válido hasta: {cert.not_valid_after_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        return True
    except Exception as e:
        print(f"  Error al procesar el certificado '{cert_name}': {e}")
        return False

def leer_certificados_dnie():
    """
    Función principal para buscar y leer los certificados específicos del DNIe.
    """
    if not os.path.exists(PKCS11_LIB_PATH):
        print(f"Error: No se encontró la librería en la ruta: {PKCS11_LIB_PATH}")
        return

    print(f"Usando librería: {PKCS11_LIB_PATH}")

    try:
        pkcs11 = pkcs11_lib(PKCS11_LIB_PATH)
        slots = pkcs11.get_slots(token_present=True)
        if not slots:
            print("\nError: No se encontró lector o DNIe.")
            return

        token = slots[0].get_token()
        print("\n¡DNIe detectado!")
        print("Buscando certificados específicos...\n" + "="*40)

        found_count = 0
        with token.open(rw=False) as session:
            # --- BÚSQUEDA ESPECÍFICA POR ETIQUETA (LABEL) ---
            # 1. Buscar el certificado de Autenticación
            auth_cert = next(session.get_objects({
                Attribute.CLASS: ObjectClass.CERTIFICATE,
                Attribute.LABEL: 'CertAutenticacion'
            }), None)

            if auth_cert:
                if parse_and_print_certificate(auth_cert, "Autenticación"):
                    found_count += 1
            else:
                print("\n- No se encontró el Certificado de Autenticación.")

            # 2. Buscar el certificado de Firma
            sign_cert = next(session.get_objects({
                Attribute.CLASS: ObjectClass.CERTIFICATE,
                Attribute.LABEL: 'CertFirmaDigital'
            }), None)

            if sign_cert:
                if parse_and_print_certificate(sign_cert, "Firma Digital"):
                    found_count += 1
            else:
                print("\n- No se encontró el Certificado de Firma Digital.")

        print("\n" + "="*40 + f"\nBúsqueda completada. Se encontraron y procesaron {found_count} certificados válidos.")

    except Exception as e:
        print(f"\nHa ocurrido un error inesperado durante la conexión: {e}")

# --- Punto de entrada del programa ---
if __name__ == "__main__":
    leer_certificados_dnie()