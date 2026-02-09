import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# 1. 비밀번호 확인 로직 (시크릿 금고 사용) 🔑
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    def password_entered():
        # st.secrets["MY_PWD"]를 사용하여 금고에서 비번을 가져옵니다.
        if st.session_state["pwd_input"] == st.secrets["MY_PWD"]:
            st.session_state["password_correct"] = True
            del st.session_state["pwd_input"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.title("🔒 Access Required")
    st.text_input(
        "비밀번호를 입력하고 엔터를 누르세요", 
        type="password", 
        on_change=password_entered, 
        key="pwd_input"
    )

    if st.session_state.get("password_correct") == False and "pwd_input" not in st.session_state:
        st.error("😕 비밀번호가 틀렸습니다. 다시 시도하세요.")
    
    return False

# 2. 메인 앱 실행 제어 🚀
if check_password():
    st.title("💳 Payment Receipt Tool")
    
    # --- 이하 영수증 도구 기능 동일 ---
    with st.container():
        st.subheader("📝 Enter Details")
        col1, col2 = st.columns(2)
        with col1:
            vendor_list = ["VITERRA", "VOITA", "M&M", "TFC", "PREMIER", "CAPESPAN"]
            vendor = st.selectbox("Vendor", vendor_list)
            date = st.date_input("Date", datetime.now())
            inv_no = st.text_input("Invoice No", "520")
            item = st.text_input("Item", "CHILE CHERRY")
            ref_no = st.text_input("Ref No.", "CHCH26003")
        with col2:
            total_amt = st.number_input("Total Amount ($)", min_value=0.0, value=99636.00)
            prev_pay = st.number_input("Previous Payment ($)", min_value=0.0, value=0.0)
            curr_remit = st.number_input("Current Remittance ($)", min_value=0.0, value=40000.00)
            ex_rate = st.number_input("Ex. Rate", min_value=0.0, value=1460.30)

    balance = total_amt - prev_pay - curr_remit
    krw_total = curr_remit * ex_rate
    formatted_date = date.strftime('%b %d, %Y')
    st.markdown("---")

    receipt_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background-color: transparent; }}
        #capture-target {{ background-color: #f0f2f6; padding: 30px; display: inline-block; border-radius: 12px; border: 0.5px solid #e0e0e0; }}
        .receipt-card {{ background-color: white; padding: 25px; border-radius: 12px; border: 1px solid #ddd; box-shadow: 0 8px 16px rgba(0,0,0,0.08); width: 380px; margin: auto; }}
        .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 12px; margin-bottom: 20px; }}
        .row {{ display: flex; justify-content: space-between; margin-bottom: 10px; }}
        .row-highlight {{ display: flex; justify-content: space-between; margin-bottom: 10px; background-color: #ffff99; padding: 5px 10px; border-radius: 6px; margin-left: -10px; margin-right: -10px; }}
        .label {{ color: #666; font-size: 14px; }}
        .value {{ font-size: 15px; font-weight: bold; }}
        .divider {{ border: none; border-top: 1px dashed #eee; margin: 15px 0; }}
        .total-box {{ text-align: right; background: #f1f8ff; padding: 15px; border-radius: 8px; border-right: 4px solid #007bff; }}
        .btn-container {{ text-align: center; margin-top: 20px; }}
        .btn {{ border: none; color: white; padding: 12px 20px; font-size: 14px; cursor: pointer; border-radius: 8px; box-shadow: 0 4px #999; margin: 0 5px; }}
        .download-btn {{ background-color: #4CAF50; }}
        .copy-btn {{ background-color: #008CBA; }}
    </style>
    </head>
    <body>
    <div style="text-align: center;">
        <div id="capture-target">
            <div class="receipt-card">
                <div class="header"><h1>PAYMENT DETAILS</h1><small>{formatted_date}</small></div>
                <div class="row"><span class="label">Vendor:</span><span class="value">{vendor}</span></div>
                <div class="row"><span class="label">Date:</span><span class="value">{formatted_date}</span></div>
                <div class="row"><span class="label">Invoice No:</span><span class="value">{inv_no}</span></div>
                <div class="row"><span class="label">Item:</span><span class="value">{item}</span></div>
                <div class="row"><span class="label">Ref No:</span><span class="value">{ref_no}</span></div>
                <hr class="divider">
                <div class="row"><span class="label">Total Amount:</span><span class="value">$ {total_amt:,.2f}</span></div>
                <div class="row"><span class="label">Previous Payment:</span><span class="value">$ {prev_pay:,.2f}</span></div>
                <div class="row-highlight"><span class="label">Current Remittance:</span><span class="value">$ {curr_remit:,.2f}</span></div>
                <div class="row"><span class="label">Balance:</span><span class="value">$ {balance:,.2f}</span></div>
                <hr class="divider">
                <div class="total-box"><small>FINAL KRW TOTAL (Rate: {ex_rate:,.2f})</small><br><b>₩ {int(krw_total):,}</b></div>
            </div>
        </div>
    </div>
    <div class="btn-container">
        <button class="btn download-btn" onclick="downloadReceipt()">📸 Save JPG</button>
        <button class="btn copy-btn" onclick="copyReceipt()">📋 Copy Image</button>
    </div>
    <script>
        function downloadReceipt() {{
            html2canvas(document.getElementById('capture-target'), {{ scale: 2 }}).then(canvas => {{
                var link = document.createElement('a');
                link.download = 'payment_{vendor}.jpg';
                link.href = canvas.toDataURL("image/jpeg", 0.9);
                link.click();
            }});
        }}
        async function copyReceipt() {{
            const canvas = await html2canvas(document.getElementById('capture-target'), {{ scale: 2 }});
            canvas.toBlob(blob => {{
                navigator.clipboard.write([new ClipboardItem({{ "image/png": blob }})]);
            }});
        }}
    </script>
    </body>
    </html>
    """
    components.html(receipt_html, height=760)
