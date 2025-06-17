<odoo>
    <data>
        <!-- Legal Document Version List View -->
        <record id="view_influence_gen_legal_document_version_tree" model="ir.ui.view">
            <field name="name">influence.gen.legal.document.version.tree</field>
            <field name="model">influence_gen.legal_document_version</field>
            <field name="arch" type="xml">
                <tree string="Legal Document Versions" decoration-bf="is_active==True">
                    <field name="document_type"/>
                    <field name="version"/>
                    <field name="effective_date"/>
                    <field name="is_active" widget="boolean_toggle"/>
                </tree>
            </field>
        </record>

        <!-- Legal Document Version Form View -->
        <record id="view_influence_gen_legal_document_version_form" model="ir.ui.view">
            <field name="name">influence.gen.legal.document.version.form</field>
            <field name="model">influence_gen.legal_document_version</field>
            <field name="arch" type="xml">
                <form string="Legal Document Version">
                    <sheet>
                        <group>
                            <group>
                                <field name="document_type"/>
                                <field name="version"/>
                            </group>
                            <group>
                                <field name="effective_date"/>
                                <field name="is_active"/>
                                <field name="attachment_id" widget="many2one_binary" filename="attachment_filename"/>
                                <field name="attachment_filename" invisible="1"/>
                            </group>
                        </group>
                        <notebook>
                            <page string="Content">
                                <field name="content" widget="html"/>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- Legal Document Version Action Window -->
        <record id="action_influence_gen_legal_document_version" model="ir.actions.act_window">
            <field name="name">Legal Document Versions</field>
            <field name="res_model">influence_gen.legal_document_version</field>
            <field name="view_mode">tree,form</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Create a new Legal Document Version.
                </p><p>
                    Manage versions of your Terms of Service and Privacy Policy.
                </p>
            </field>
        </record>
    </data>
</odoo>