"""
Healthcare Data Warehouse - Interactive SQL Query & Visualization Web UI
Apache 2.0 Licensed Framework (Flask + Plotly)

Features:
- Write custom SQL queries in the browser
- Instant table results
- Automatic graph generation (Line, Bar, Pie charts)
- Pre-built analysis templates
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import json

app = Flask(__name__)

# Database connection
DATABASE_URL = "postgresql://admin:admin@localhost:5432/healthcare_dw"
engine = create_engine(DATABASE_URL)

# Pre-built SQL query templates
QUERY_TEMPLATES = {
    'disease_distribution': {
        'name': '🦠 Disease Distribution',
        'sql': '''SELECT 
    d.medical_condition,
    COUNT(*) as case_count,
    AVG(f.billing_amount) as avg_cost
FROM fact_admissions f
JOIN dim_disease d ON f.disease_id = d.disease_id
GROUP BY d.medical_condition
ORDER BY case_count DESC;''',
        'chart_type': 'pie'
    },
    'monthly_trends': {
        'name': '📈 Monthly Admission Trends',
        'sql': '''SELECT 
    t.year,
    t.month,
    COUNT(*) as admissions,
    AVG(f.billing_amount) as avg_billing
FROM fact_admissions f
JOIN dim_time t ON f.time_id = t.time_id
GROUP BY t.year, t.month
ORDER BY t.year, t.month;''',
        'chart_type': 'line'
    },
    'age_distribution': {
        'name': '👥 Age Group Distribution',
        'sql': '''SELECT 
    CASE 
        WHEN p.age < 18 THEN '0-17'
        WHEN p.age BETWEEN 18 AND 35 THEN '18-35'
        WHEN p.age BETWEEN 36 AND 55 THEN '36-55'
        WHEN p.age BETWEEN 56 AND 70 THEN '56-70'
        ELSE '70+'
    END as age_group,
    COUNT(*) as patient_count
FROM fact_admissions f
JOIN dim_patient p ON f.patient_id = p.patient_id
GROUP BY age_group
ORDER BY age_group;''',
        'chart_type': 'bar'
    },
    'hospital_revenue': {
        'name': '🏥 Hospital Revenue',
        'sql': '''SELECT 
    h.hospital_name,
    SUM(f.billing_amount) as total_revenue,
    COUNT(*) as admissions
FROM fact_admissions f
JOIN dim_hospital h ON f.hospital_id = h.hospital_id
GROUP BY h.hospital_name
ORDER BY total_revenue DESC
LIMIT 15;''',
        'chart_type': 'bar'
    },
    'insurance_claims': {
        'name': '💼 Insurance Provider Claims',
        'sql': '''SELECT 
    i.insurance_provider,
    COUNT(*) as total_claims,
    SUM(f.billing_amount) as total_amount,
    AVG(f.billing_amount) as avg_claim
FROM fact_admissions f
JOIN dim_insurance i ON f.insurance_id = i.insurance_id
GROUP BY i.insurance_provider
ORDER BY total_amount DESC;''',
        'chart_type': 'pie'
    },
    'gender_disease': {
        'name': '⚧ Gender vs Disease',
        'sql': '''SELECT 
    p.gender,
    d.medical_condition,
    COUNT(*) as count
FROM fact_admissions f
JOIN dim_patient p ON f.patient_id = p.patient_id
JOIN dim_disease d ON f.disease_id = d.disease_id
GROUP BY p.gender, d.medical_condition
ORDER BY count DESC;''',
        'chart_type': 'bar'
    },
    'seasonal_trends': {
        'name': '🌦️ Seasonal Admission Patterns',
        'sql': '''SELECT 
    CASE 
        WHEN t.month IN (12, 1, 2) THEN 'Winter'
        WHEN t.month IN (3, 4, 5) THEN 'Spring'
        WHEN t.month IN (6, 7, 8) THEN 'Summer'
        ELSE 'Fall'
    END as season,
    COUNT(*) as admissions,
    AVG(f.billing_amount) as avg_cost
FROM fact_admissions f
JOIN dim_time t ON f.time_id = t.time_id
GROUP BY season
ORDER BY admissions DESC;''',
        'chart_type': 'bar'
    },
    'top_doctors': {
        'name': '👨‍⚕️ Top Doctors by Patient Load',
        'sql': '''SELECT 
    d.doctor_name,
    COUNT(*) as patient_count,
    AVG(f.billing_amount) as avg_billing
FROM fact_admissions f
JOIN dim_doctor d ON f.doctor_id = d.doctor_id
GROUP BY d.doctor_name
ORDER BY patient_count DESC
LIMIT 15;''',
        'chart_type': 'bar'
    }
}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', templates=QUERY_TEMPLATES)

@app.route('/execute_query', methods=['POST'])
def execute_query():
    """Execute SQL query and return results with visualization"""
    try:
        data = request.json
        sql_query = data.get('query', '')
        chart_type = data.get('chart_type', 'auto')
        
        # Execute query
        df = pd.read_sql(sql_query, engine)
        
        if df.empty:
            return jsonify({
                'success': False,
                'error': 'Query returned no results'
            })
        
        # Convert DataFrame to dict for JSON
        table_data = df.to_dict('records')
        columns = df.columns.tolist()
        
        # Generate chart
        chart_json = generate_chart(df, chart_type)
        
        return jsonify({
            'success': True,
            'columns': columns,
            'data': table_data,
            'row_count': len(df),
            'chart': chart_json,
            'chart_generated': bool(chart_json)
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })

def generate_chart(df, chart_type='auto'):
    """Generate appropriate chart based on data"""
    
    if len(df) == 0:
        return '<p>No data to visualize</p>'
    
    # Auto-detect chart type if not specified
    if chart_type == 'auto':
        if len(df.columns) == 2:
            # If second column is numeric, use bar chart
            if pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
                chart_type = 'bar'
            else:
                chart_type = 'table'
        else:
            chart_type = 'bar'
    
    try:
        # Create visualization based on type
        if chart_type == 'pie':
            fig = create_pie_chart(df)
        elif chart_type == 'line':
            fig = create_line_chart(df)
        elif chart_type == 'bar':
            fig = create_bar_chart(df)
        else:
            return None
        
        # Return JSON for client-side rendering
        return fig.to_json()
        
    except Exception as e:
        print(f"Error generating chart: {e}")
        return None

def create_pie_chart(df):
    """Create pie chart from data"""
    if len(df.columns) < 2:
        raise ValueError("Need at least 2 columns for pie chart")
    
    labels_col = df.columns[0]
    
    # Find first numeric column
    numeric_cols = [col for col in df.columns[1:] if pd.api.types.is_numeric_dtype(df[col])]
    if not numeric_cols:
        raise ValueError("Need at least one numeric column for pie chart")
    
    values_col = numeric_cols[0]
    
    fig = px.pie(
        df,
        names=labels_col,
        values=values_col,
        title=f'{values_col} by {labels_col}',
        hole=0.3
    )
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percent: %{percent}<extra></extra>'
    )
    fig.update_layout(height=500)
    return fig

def create_line_chart(df):
    """Create line chart from data"""
    if len(df.columns) < 2:
        raise ValueError("Need at least 2 columns for line chart")
    
    # For time series with year/month, combine them
    if 'year' in df.columns and 'month' in df.columns:
        df['period'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
        x_col = 'period'
        # Use the third column (usually the count/metric)
        y_col = df.columns[2] if len(df.columns) > 2 else df.columns[1]
    else:
        x_col = df.columns[0]
        y_col = df.columns[1]
    
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=f'{y_col} over {x_col}',
        markers=True
    )
    fig.update_layout(
        height=500, 
        hovermode='x unified',
        xaxis_title=x_col,
        yaxis_title=y_col
    )
    return fig

def create_bar_chart(df):
    """Create bar chart from data"""
    if len(df.columns) < 2:
        raise ValueError("Need at least 2 columns for bar chart")
    
    x_col = df.columns[0]
    
    # Find the first numeric column for y-axis
    numeric_cols = [col for col in df.columns[1:] if pd.api.types.is_numeric_dtype(df[col])]
    if not numeric_cols:
        raise ValueError("Need at least one numeric column for bar chart")
    
    y_col = numeric_cols[0]
    
    # Check if we have multiple numeric columns (grouped bar chart)
    if len(numeric_cols) > 1 and len(numeric_cols) <= 5:  # Limit to 5 series for readability
        fig = go.Figure()
        for col in numeric_cols:
            fig.add_trace(go.Bar(name=col, x=df[x_col], y=df[col]))
        fig.update_layout(
            title=f'Comparison across {x_col}',
            barmode='group',
            height=500,
            xaxis_title=x_col,
            yaxis_title='Values',
            xaxis_tickangle=-45
        )
    else:
        # Single bar chart with color gradient
        fig = px.bar(
            df,
            x=x_col,
            y=y_col,
            title=f'{y_col} by {x_col}',
            color=y_col,
            color_continuous_scale='Viridis',
            text=y_col
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(
            height=500, 
            xaxis_tickangle=-45,
            xaxis_title=x_col,
            yaxis_title=y_col
        )
    
    return fig

@app.route('/get_schema')
def get_schema():
    """Get database schema information"""
    try:
        schema_query = """
        SELECT 
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        df = pd.read_sql(schema_query, engine)
        
        # Group by table
        schema_dict = {}
        for table in df['table_name'].unique():
            schema_dict[table] = df[df['table_name'] == table][['column_name', 'data_type']].to_dict('records')
        
        return jsonify({'success': True, 'schema': schema_dict})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("=" * 80)
    print("🏥 Healthcare Data Warehouse - Interactive SQL Analytics UI")
    print("=" * 80)
    print("\n🌐 Starting web server...")
    print("📊 Access the dashboard at: http://localhost:5000")
    print("\n✨ Features:")
    print("   • Write custom SQL queries")
    print("   • Instant table results")
    print("   • Automatic graph generation")
    print("   • Pre-built analysis templates")
    print("\n" + "=" * 80)
    app.run(debug=True, host='0.0.0.0', port=5000)
